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

package io.github.mobotx.Mobot.AssetManager.Assets.Imu

import android.hardware.Sensor
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import io.github.mobotx.*
import io.grpc.ManagedChannel

class Accelerometer(private val activity: AppCompatActivity,
                    private val imu: Imu): MotionSensor(activity, imu, Sensor.TYPE_ACCELEROMETER) {

    private lateinit var stub: AccelerometerGrpc.AccelerometerBlockingStub

    fun start(channel: ManagedChannel){
        this.stub = AccelerometerGrpc.newBlockingStub(channel)
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
            val reply = stub.setAccelerometerMetadata(metadataMsg)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        if(success){
            Log.d("Mobot", "Accelerometer: Metadata Set")
        }else{
            Log.d("Mobot", "Accelerometer: Failed to Set Metadata")
        }
        return success
    }

    override fun sendData(data: FloatArray): Boolean {
        var success: Boolean

        val ax = data[0]
        val ay = data[1]
        val az = data[2]
        val linearAccelerationMsg = Vector3.newBuilder().setX(ax).setY(ay).setZ(az).build()

        try{
            val reply = stub.newAccelerometerData(linearAccelerationMsg)
            success = reply.success
        }catch (e: io.grpc.StatusRuntimeException){
            success = false
        }
        return success
    }
}