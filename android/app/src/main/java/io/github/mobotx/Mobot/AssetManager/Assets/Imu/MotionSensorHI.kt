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

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import androidx.appcompat.app.AppCompatActivity
import androidx.core.text.buildSpannedString
import io.github.mobotx.Mobot.utils.Rate
import io.github.mobotx.R

class MotionSensorHI(private val activity: AppCompatActivity,
                     private val motionSensor: MotionSensor,
                     private val sensorType:Int): SensorEventListener {

    private var sensorManager: SensorManager = activity.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    var available = false // STATE VARIABLE
    private lateinit var sensor : Sensor

    init {
        if (sensorManager.getDefaultSensor(sensorType) != null) {
            available = true
            sensor = sensorManager.getDefaultSensor(sensorType)
        }
    }

    override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) {
        //TODO
    }

    override fun onSensorChanged(event: SensorEvent) {
        if(event.sensor.type == sensorType) {
            motionSensor.sensorEvent(event.values)
        }
    }

    fun start(){
        sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_GAME)
    }

    fun stop(){
        sensorManager.unregisterListener(this, sensor)
    }

    fun getMetadata(): MotionSensorMetadata{
        return MotionSensorMetadata(sensor.vendor,
                sensor.version.toFloat(),
                sensor.resolution,
                sensor.maximumRange)
    }
}