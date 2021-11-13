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

import android.Manifest
import android.annotation.SuppressLint
import android.hardware.camera2.CameraMetadata.CONTROL_AF_MODE_OFF
import android.hardware.camera2.CaptureRequest
import android.util.Log
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.camera2.interop.Camera2CameraControl
import androidx.camera.camera2.interop.CaptureRequestOptions
import androidx.camera.core.CameraControl
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.impl.CameraConfig
import androidx.camera.core.impl.Config
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import java.util.concurrent.Executors

class CameraSystemHI(private val activity: AppCompatActivity){
    private val cameraProviderFuture = ProcessCameraProvider.getInstance(activity)

    private val imageAnalysis = ImageAnalysis.Builder()
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .build()

    private val cameraProvider = cameraProviderFuture.get()

    private val cameraSelector = CameraSelector.Builder()
            .requireLensFacing(CameraSelector.LENS_FACING_BACK)
            .build()

    private val executor = Executors.newSingleThreadExecutor()

    private lateinit var cam: androidx.camera.core.Camera
    private lateinit var camera: Camera

    private var active = false

    var available = false // STATE VARIABLE
    var flashlightAvailable = false // STATE VARIABLE

    private val activityResultLauncher =
            activity.registerForActivityResult(
                    ActivityResultContracts.RequestPermission()){ isGranted ->
                available = isGranted
                camera.onStateChange()
            }

    fun init() {
        activityResultLauncher.launch(Manifest.permission.CAMERA)

        cameraProviderFuture.addListener(Runnable {
            imageAnalysis.setAnalyzer(executor, ImageAnalysis.Analyzer { image ->
                if(active) {
                    camera.cameraEvent(image)
                }
                image.close()
            })

        }, ContextCompat.getMainExecutor(activity))

        activity.runOnUiThread {
            cam = cameraProvider.bindToLifecycle(activity as LifecycleOwner, cameraSelector, imageAnalysis)
        }

        flashlightAvailable = cam.cameraInfo.hasFlashUnit()
        Log.d("Mobot", cam.cameraControl.toString())
    }

    @SuppressLint("UnsafeOptInUsageError")
    fun setFocus(f:Float){
        val cameraControl : CameraControl = cam.cameraControl
        val camera2CameraControl : Camera2CameraControl = Camera2CameraControl.from(cameraControl)
        val captureRequestOptions = CaptureRequestOptions.Builder()
                .setCaptureRequestOption(CaptureRequest.CONTROL_AF_MODE, CaptureRequest.CONTROL_AF_MODE_OFF)
                .setCaptureRequestOption(CaptureRequest.LENS_FOCUS_DISTANCE, f)
                .build()
        camera2CameraControl.captureRequestOptions = captureRequestOptions
    }

    fun start(){
        active = true
        setFocus(0.2f)
    }

    fun stop(){
        active = false
    }

    fun setCameraHdl(camera: Camera){
        this.camera = camera
    }

    fun setFlashlightState(on:Boolean){
        if (flashlightAvailable){
            cam.cameraControl.enableTorch(on)
        }
    }

    fun getMetadata():CameraMetadata{
        return CameraMetadata(480,640,3,8)
    }
}
