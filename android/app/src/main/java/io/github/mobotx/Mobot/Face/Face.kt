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

package io.github.mobotx.Mobot.Face

import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import io.github.mobotx.Mobot.AssetManager.AssetManager
import io.github.mobotx.Mobot.Connection.Connection
import io.github.mobotx.Mobot.utils.Rate
import io.github.mobotx.R

class Face(private val activity: AppCompatActivity) {
    private val faceView = activity.findViewById<ImageButton>(R.id.face)
    private val faceTextView = activity.findViewById<TextView>(R.id.faceText)

    private var lost = false
    private var connected = false
    private var chassisAvailable = false

    private lateinit var connection: Connection
    private lateinit var assetManager: AssetManager

    private val face_hz = activity.getString(R.string.face_hz).toDouble()

    init {
        refreshUI()
    }

    fun start(){
        Thread(Runnable {
            val rate = Rate(face_hz)
            while (true) {
                if (connection.connectionState == Connection.ConnectionState.LOST) {
                    lost = true
                }else{
                    lost = false
                    if (connection.connectionState == Connection.ConnectionState.CONNECTED){
                        connected = true
                        chassisAvailable = assetManager.chassis.chassisHI.available
                    }else{
                        connected = false
                    }
                }
                refreshUI()
                rate.sleep()
            }
        }).start()
    }

    private fun refreshUI(){
        activity.runOnUiThread {
            if (lost) {
                faceView.setImageResource(R.drawable.mobot_sad)
                faceTextView.text = activity.getString(R.string.face_text_lost)
            }else {
                if (connected) {
                    if (chassisAvailable) {
                        faceView.setImageResource(R.drawable.mobot_happy)
                        faceTextView.text = activity.getString(R.string.face_text_happy)
                    } else {
                        faceView.setImageResource(R.drawable.mobot_awake)
                        faceTextView.text = activity.getString(R.string.face_text_awake)
                    }
                } else {
                    faceView.setImageResource(R.drawable.mobot_sleepy)
                    faceTextView.text = activity.getString(R.string.face_text_asleep)
                }
            }
        }
    }

    fun setAssetManagerHdl(assetManager: AssetManager){
        this.assetManager = assetManager
    }

    fun setConnectionHdl(connection: Connection){
        this.connection = connection
    }
}