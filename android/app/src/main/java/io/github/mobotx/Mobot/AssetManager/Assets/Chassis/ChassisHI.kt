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

package io.github.mobotx.Mobot.AssetManager.Assets.Chassis

import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.hardware.usb.UsbDevice
import android.hardware.usb.UsbDeviceConnection
import android.hardware.usb.UsbManager
import com.felhr.usbserial.UsbSerialDevice
import com.felhr.usbserial.UsbSerialInterface
import io.github.mobotx.MainActivity

class ChassisHI(private val activity: MainActivity, private val chassis: Chassis) {
    var available: Boolean = false // STATE VARIABLE

    private var usbManager: UsbManager = activity.getSystemService(Context.USB_SERVICE) as UsbManager
    private var usbDevice: UsbDevice? = null
    private var usbSerialDevice: UsbSerialDevice? = null
    private var usbDeviceConnection: UsbDeviceConnection? = null
    private val ACTION_USB_PERMISSION = "permission"

    private val broadcastReceiver = object : BroadcastReceiver(){
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action!! == ACTION_USB_PERMISSION) {
                val granted: Boolean = intent.extras!!.getBoolean(UsbManager.EXTRA_PERMISSION_GRANTED)
                if (granted) {
                    usbDeviceConnection = usbManager.openDevice(usbDevice)
                    usbSerialDevice = UsbSerialDevice.createUsbSerialDevice(usbDevice, usbDeviceConnection)
                    if (usbSerialDevice != null) {
                        if (usbSerialDevice!!.open()) {
                            usbSerialDevice!!.setBaudRate(115200)
                            usbSerialDevice!!.setDataBits(UsbSerialInterface.DATA_BITS_8)
                            usbSerialDevice!!.setStopBits(UsbSerialInterface.STOP_BITS_1)
                            usbSerialDevice!!.setParity(UsbSerialInterface.PARITY_NONE)
                            usbSerialDevice!!.setFlowControl(UsbSerialInterface.FLOW_CONTROL_OFF)
                        }
                    }
                }
            } else if (intent.action == UsbManager.ACTION_USB_DEVICE_ATTACHED) {
                startUsbConnecting()
                activity.beforeActivityRestarts()
            } else if (intent.action == UsbManager.ACTION_USB_DEVICE_DETACHED) {
                disconnect()
            }
        }
    }

    init {
        val filter = IntentFilter()
        filter.addAction(ACTION_USB_PERMISSION)
        filter.addAction(UsbManager.ACTION_USB_DEVICE_ATTACHED)
        filter.addAction(UsbManager.ACTION_USB_DEVICE_DETACHED)
        activity.registerReceiver(broadcastReceiver, filter)

        startUsbConnecting()
    }

    private fun startUsbConnecting() {
        val usbDevices = usbManager.deviceList
        if (!usbDevices?.isEmpty()!!) {
            usbDevices.forEach { _, dev ->
                if (!available) {
                    val deviceVendorId: Int? = dev?.vendorId
                    val productId: Int? = dev?.productId
                    val serialNumber = dev?.serialNumber
                    if (deviceVendorId == 4292 && productId == 60000 && serialNumber == "0001") {
                        usbDevice = dev
                        val intent: PendingIntent = PendingIntent.getBroadcast(activity, 0, Intent(ACTION_USB_PERMISSION), 0)
                        usbManager.requestPermission(usbDevice, intent)
                        available = true
                    }
                }
            }
        }
    }

    private fun disconnect() {
        available = false
        chassis.chassisHIUnavailable()
        usbSerialDevice?.close()
    }

    fun setCmdVel(wr: Float, wl:Float){
        val msg = "CMDVEL:$wr,$wl\r"
        usbSerialDevice?.write(msg.toByteArray())
    }

    private fun readLine():String{
        var line:String = ""
        val byte:ByteArray = ByteArray(1)
        while(true) {
            val n = usbSerialDevice?.syncRead(byte, 0)
            if(n == 1){
                val ch = byte[0].toChar()
                if(ch == '\r'){
                    break
                }else{
                    line += ch
                }
            }
        }
        return line
    }

    // TODO: Add Timeout
    fun getMetadata():ChassisMetadata{
        usbSerialDevice?.write("GET:Metadata\r".toByteArray())
        while(true){
            val msg = readLine()
            val msg_split = msg.split(':')
            if(msg_split[0] == "METADATA"){
                val data = msg_split[1].split(',')
                val wheelDiameter = data[0].toFloat()
                val wheelToWheelSeparation = data[1].toFloat()
                val maxWheelSpeed = data[2].toFloat()
                val minWheelSpeed = data[3].toFloat()
                return ChassisMetadata(wheelDiameter, wheelToWheelSeparation, maxWheelSpeed, minWheelSpeed)
            }
        }
    }
}
