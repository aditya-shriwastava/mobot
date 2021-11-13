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

package io.github.mobotx.Mobot.AssetManager.Assets.CameraSystem

import android.widget.ImageView
import io.github.mobotx.*
import io.grpc.ManagedChannel
import io.grpc.StatusRuntimeException

class Flashlight(private val activity: MainActivity) {
    private val flashlightView: ImageView = activity.findViewById<ImageView>(R.id.flashlight)

    var connected: Boolean = false // STATE VARIABLE

    private lateinit var cameraSystemHI: CameraSystemHI
    private lateinit var stub: FlashlightGrpc.FlashlightBlockingStub

    fun start(channel: ManagedChannel){
        if (cameraSystemHI.flashlightAvailable) {
            connected = true
            stub = FlashlightGrpc.newBlockingStub(channel)
            Thread(Runnable {
                getFlashlightCmdStream()
            }).start()
            refreshUI()
        }
    }

    fun stop(){
        if(connected) {
            connected = false
            cameraSystemHI.setFlashlightState(false)
            refreshUI()
        }
    }

    fun setCameraHIHdl(cameraSystemHI: CameraSystemHI){
        this.cameraSystemHI = cameraSystemHI
    }

    private fun getFlashlightCmdStream(){
        try {
            val flashlightCmdIterator = stub.flashlightCmdStream(Empty.newBuilder().build())
            flashlightCmdIterator.forEachRemaining{ flashlightCmd ->
                if (cameraSystemHI.flashlightAvailable) {
                    cameraSystemHI.setFlashlightState(flashlightCmd.on)
                }
            }
        }catch (e: StatusRuntimeException){
            stop()
        }
    }

    fun refreshUI(){
        activity.runOnUiThread {
            if (cameraSystemHI.flashlightAvailable){
                flashlightView.setImageResource(R.drawable.flashlight_not_streaming)
                if (connected){
                    flashlightView.setImageResource(R.drawable.flashlight_streaming)
                }
            }else{
                flashlightView.setImageResource(R.drawable.flashlight_not_available)
            }
        }
    }
}