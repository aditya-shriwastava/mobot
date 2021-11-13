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

import android.widget.ImageView
import io.github.mobotx.MainActivity
import io.github.mobotx.Mobot.AssetManager.Assets.Imu.Gyroscope.Gyroscope
import io.github.mobotx.Mobot.AssetManager.Assets.Imu.Magnetometer.Magnetometer
import io.github.mobotx.R
import io.grpc.ManagedChannel

class Imu (private val activity: MainActivity){
    private val imuView: ImageView = activity.findViewById<ImageView>(R.id.imu)

    val accelerometer = Accelerometer(activity, this) // HOLDS STATE
    val gyroscope = Gyroscope(activity, this) // HOLDS STATE
    val magnetometer = Magnetometer(activity, this) // HOLDS STATE

    init {
        refreshUI()
    }

    fun start(channel:ManagedChannel){
        accelerometer.start(channel)
        gyroscope.start(channel)
        magnetometer.start(channel)
    }

    fun stop(){
        accelerometer.stop()
        gyroscope.stop()
        magnetometer.stop()
    }

    fun onStateChange(){
        refreshUI()
    }

    private fun refreshUI(){
        activity.runOnUiThread {
            if (accelerometer.sensorHI.available || gyroscope.sensorHI.available || magnetometer.sensorHI.available){
                imuView.setImageResource(R.drawable.imu_not_streaming)
                if (accelerometer.connected || gyroscope.connected || magnetometer.connected){
                    imuView.setImageResource(R.drawable.imu_streaming)
                }
            }else{
                imuView.setImageResource(R.drawable.imu_not_available)
            }
        }
    }
}
