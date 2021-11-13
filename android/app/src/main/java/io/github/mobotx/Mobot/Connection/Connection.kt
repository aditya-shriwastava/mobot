//MIT License
//
//Copyright (c) 2021 Mobotx
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in all
//copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.

package io.github.mobotx.Mobot.Connection

import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.android.material.textfield.TextInputEditText
import io.github.mobotx.*
import io.github.mobotx.Mobot.AssetManager.AssetManager
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import io.grpc.StatusRuntimeException
import java.util.concurrent.TimeUnit

class Connection(private val activity: AppCompatActivity) {
    private val ipView = activity.findViewById<TextInputEditText>(R.id.ip)
    private val portView = activity.findViewById<TextInputEditText>(R.id.port)
    private val buttonView = activity.findViewById<Button>(R.id.button)
    init {
        buttonView.setOnClickListener( object : View.OnClickListener{
            override fun onClick(v: View?) {
                onButtonClick()
            }
        })
    }
    private val statusView = activity.findViewById<TextView>(R.id.status)

    private lateinit var assetManager: AssetManager

    private val lastConnection = LastConnection(activity)

    enum class ConnectionState {
        CONNECTED, DISCONNECTED, LOST, CONNECTING, DISCONNECTING
    }
    var connectionState = ConnectionState.DISCONNECTED // STATE VARIABLE

    private var channel: ManagedChannel? = null
    private var stub: ConnectionGrpc.ConnectionBlockingStub? = null

    init{ // Update View with saved port and ip if available
        val connectionDetail = lastConnection.loadConnectionDetail()
        if (!connectionDetail.isNull()){
            ipView.setText(connectionDetail.ip)
            portView.setText(connectionDetail.port.toString())
        }
        refreshUI()
    }

    private fun onButtonClick(){
        if (connectionState == ConnectionState.CONNECTED){
            disconnect()
        }else if (connectionState == ConnectionState.DISCONNECTED ||
                  connectionState == ConnectionState.LOST){
            connect()
        }
    }

    private fun connect(){
        connectionState = ConnectionState.CONNECTING
        refreshUI()
        Thread(Runnable {
            val connectionDetail = ConnectionDetail()
            connectionDetail.setIpAndPortIfValid(getIp(), getPort())
            if(!connectionDetail.isNull()){
                initGrpcChannelAndStub(connectionDetail)
                if(ping()){
                    Log.d("Mobot", "Body Attach to Spine")
                    connectionState = ConnectionState.CONNECTED
                    lastConnection.saveConnectionDetail(connectionDetail)
                    refreshUI()
                    val attachBodyIterator = stub!!.attachBodyStream(Empty.newBuilder().build())
                    attachBodyStream(attachBodyIterator) // Will block until body is attached
                }else{
                    Log.d("Mobot", "Body failed to Attach to Spine")
                    connectionState = ConnectionState.DISCONNECTED
                    refreshUI()
                }
            }else{
                Log.d("Mobot", "Received Invalid Ip or Port")
                connectionState = ConnectionState.DISCONNECTED
                refreshUI()
            }
        }).start()
    }

    fun disconnect(){
        if (channel == null){
            return
        }
        connectionState = ConnectionState.DISCONNECTING
        refreshUI()
        channel!!.shutdownNow()
        channel!!.awaitTermination(2, TimeUnit.SECONDS)
    }

    private fun attachBodyStream(attachBodyIterator: Iterator<URI>){
        try{
            attachBodyIterator.forEachRemaining { brainURI ->
                Log.d("Mobot", "Brain found with URI: ${brainURI.uri}")
                assetManager.start(brainURI)
            }
        }catch (e: StatusRuntimeException){
            Log.d("Mobot", "Body Detached from Spine")
            assetManager.stop()
            if (connectionState == ConnectionState.DISCONNECTING){
                connectionState = ConnectionState.DISCONNECTED
            }else{
                connectionState = ConnectionState.LOST
                channel!!.shutdownNow()
                channel!!.awaitTermination(2, TimeUnit.SECONDS)
            }
            refreshUI()
        }
    }

    private fun ping():Boolean{
        try{
            stub!!.withDeadlineAfter(2, TimeUnit.SECONDS).ping(Empty.newBuilder().build())
            return true
        }catch (e: StatusRuntimeException){
            return false
        }
    }

    private fun getIp(): String{
        return ipView.text.toString()
    }

    private fun getPort(): Int{
        val portStr = portView.text.toString()
        if (portStr == ""){
            return -1
        }else{
            return portStr.toInt()
        }
    }

    private fun initGrpcChannelAndStub(connectionDetail: ConnectionDetail){
        channel = ManagedChannelBuilder.forAddress(connectionDetail.ip, connectionDetail.port!!).usePlaintext().build()
        stub = ConnectionGrpc.newBlockingStub(channel)
    }

    private fun refreshUI(){
        activity.runOnUiThread {
            when (connectionState) {
                ConnectionState.CONNECTED -> updateUI(false, true, R.string.button_disconnect, R.string.status_connected, R.color.green)
                ConnectionState.DISCONNECTED -> updateUI(true, true, R.string.button_connect, R.string.status_disconnected, R.color.red)
                ConnectionState.LOST -> updateUI(true, true, R.string.button_connect, R.string.status_disconnected, R.color.red)
                ConnectionState.CONNECTING -> updateUI(false, false, R.string.button_connect, R.string.status_connecting, R.color.red)
                ConnectionState.DISCONNECTING -> updateUI(false, false, R.string.button_disconnect, R.string.status_disconnecting, R.color.red)
            }
        }
    }

    private fun updateUI(inputEnabled:Boolean,
                 buttonEnabled:Boolean,
                 buttonTextR:Int,
                 statusTextR:Int,
                 statusColorR: Int){
        ipView.isEnabled = inputEnabled

        portView.isEnabled = inputEnabled

        buttonView.isEnabled = buttonEnabled
        buttonView.text = activity.getString(buttonTextR)

        statusView.text = activity.getString(statusTextR)
        statusView.setTextColor(ContextCompat.getColor(activity, statusColorR))
    }

    fun setAssetManagerHdl(assetManager: AssetManager){
        this.assetManager = assetManager
    }
}