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

import androidx.appcompat.app.AppCompatActivity
import io.github.mobotx.Mobot.utils.Rate
import io.github.mobotx.R

open class MotionSensor(private val activity: AppCompatActivity, private val imu: Imu, private val sensorType:Int) {
    var connected: Boolean = false // STATE VARIABLE
    val sensorHI = MotionSensorHI(activity, this, sensorType)

    private var busy = false
    private val hz = activity.getString(R.string.imu_hz).toDouble()
    private val rate = Rate(hz)

    fun _start(){
        if(sensorHI.available){
            connected = true
            imu.onStateChange()
            Thread(Runnable {
                if (!sendMetadata()){
                    connected = false
                    imu.onStateChange()
                }else{
                    sensorHI.start()
                }
            }).start()
        }
    }

    fun stop(){
        if(connected) {
            connected = false
            imu.onStateChange()
            sensorHI.stop()
        }
    }

    fun sensorEvent(data: FloatArray){
        if (connected){
            if(!busy)
            Thread(Runnable {
                busy = true
                if (!sendData(data)) {
                    stop()
                }
                rate.sleep()
                busy = false
            }).start()
        }
    }

    open fun sendMetadata():Boolean{
        return true
    }

    open fun sendData(data: FloatArray):Boolean{
        return true
    }
}