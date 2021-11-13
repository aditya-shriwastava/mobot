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

package io.github.mobotx.Mobot.AssetManager.Assets.Imu.Magnetometer

import android.hardware.Sensor
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import io.github.mobotx.*
import io.github.mobotx.Mobot.AssetManager.Assets.Imu.Imu
import io.github.mobotx.Mobot.AssetManager.Assets.Imu.MotionSensor
import io.grpc.ManagedChannel

class Magnetometer (private val activity: AppCompatActivity,
                    private val imu: Imu): MotionSensor(activity, imu, Sensor.TYPE_ROTATION_VECTOR) {

    private lateinit var stub: MagnetometerGrpc.MagnetometerBlockingStub

    fun start(channel: ManagedChannel){
        this.stub = MagnetometerGrpc.newBlockingStub(channel)
        _start()
    }

    override fun sendMetadata():Boolean{
        val metadata = sensorHI.getMetadata()

        var success: Boolean
        val metadataMsg = SensorMetadata.newBuilder()
                .setVendor(metadata.vendor)
                .setVersion(metadata.version)
                .setResolution(metadata.resolution)
                .setMaxRange(metadata.maxRange)
                .build()

        try{
            val reply = stub.setMagnetometerMetadata(metadataMsg)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        if(success){
            Log.d("Mobot", "Magnetometer: Metadata Set")
        }else{
            Log.d("Mobot", "Magnetometer: Failed to Set Metadata")
        }
        return success
    }

    override fun sendData(data: FloatArray): Boolean {
        var success: Boolean

        val x = data[0]
        val y = data[1]
        val z = data[2]
        val w = data[3]
        val orientationMsg = Quaternion.newBuilder().setX(x).setY(y).setZ(z).setW(w).build()

        try{
            val reply = stub.newMagnetometerData(orientationMsg)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        return success
    }
}