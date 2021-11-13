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

import android.annotation.SuppressLint
import android.util.Log
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.ImageProxy
import com.google.protobuf.ByteString
import io.github.mobotx.CameraGrpc
import io.github.mobotx.CameraMetadata
import io.github.mobotx.CompressedImage
import io.github.mobotx.Mobot.utils.Rate
import io.github.mobotx.R
import io.grpc.ManagedChannel

class Camera(private val activity: AppCompatActivity) {
    private val cameraView = activity.findViewById<ImageView>(R.id.camera)

    var connected: Boolean = false // STATE VARIABLE

    private lateinit var cameraSystemHI: CameraSystemHI
    private lateinit var stub: CameraGrpc.CameraBlockingStub

    private val rate = Rate(activity.getString(R.string.camera_hz).toDouble())

    fun start(channel: ManagedChannel){
        if(cameraSystemHI.available){
            connected = true
            stub = CameraGrpc.newBlockingStub(channel)
            refreshUI()
            Thread(Runnable {
                if (!sendMetadata()){
                    connected = false
                }else{
                    cameraSystemHI.start()
                }
                refreshUI()
            }).start()
        }
    }

    fun stop(){
        if(connected) {
            connected = false
            cameraSystemHI.stop()
            refreshUI()
        }
    }

    fun setCameraHIHdl(cameraSystemHI: CameraSystemHI){
        this.cameraSystemHI = cameraSystemHI
    }

    @SuppressLint("UnsafeOptInUsageError")
    fun cameraEvent(image: ImageProxy){
        if (connected){
            var jpegImage: ByteArray? = image.image?.let { toJpegImage(it, 80) }
            if (jpegImage != null) {
                if (!sendImage(jpegImage)) {
                    stop()
                }
            }
        }
        rate.sleep()
    }

    private fun sendMetadata():Boolean{
        var success: Boolean
        val cameraMetadata = cameraSystemHI.getMetadata()
        val metadata = CameraMetadata.newBuilder()
                .setWidth(cameraMetadata.width)
                .setHeight(cameraMetadata.height)
                .setChannels(cameraMetadata.channels)
                .setColorDepth(cameraMetadata.colorDepth)
                .build()

        try{
            val reply = stub.setCameraMetadata(metadata)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        if(success){
            Log.d("Mobot", "Camera: Metadata Set")
        }else{
            Log.d("Mobot", "Camera: Failed to Set Metadata")
        }
        return success
    }

    private fun sendImage(jpegImage:ByteArray):Boolean{
        var success: Boolean

        val compressedImage = CompressedImage.newBuilder()
                .setData(ByteString.copyFrom(jpegImage))
                .build()

        try{
            val reply = stub.newCameraData(compressedImage)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        return success
    }

    fun onStateChange(){
        refreshUI()
    }

    fun refreshUI(){
        activity.runOnUiThread {
            if (cameraSystemHI.available){
                cameraView.setImageResource(R.drawable.camera_not_streaming)
                if (connected){
                    cameraView.setImageResource(R.drawable.camera_streaming)
                }
            }else{
                cameraView.setImageResource(R.drawable.camera_not_available)
            }
        }
    }
}
