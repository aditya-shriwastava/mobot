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

package io.github.mobotx.Mobot.AssetManager

import io.github.mobotx.MainActivity
import io.github.mobotx.Mobot.AssetManager.Assets.CameraSystem.CameraSystem
import io.github.mobotx.Mobot.AssetManager.Assets.Chassis.Chassis
import io.github.mobotx.Mobot.AssetManager.Assets.Imu.Imu
import io.github.mobotx.URI
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder

class AssetManager(private val activity: MainActivity) {
    private var channel: ManagedChannel? = null
    val cameraSystem = CameraSystem(activity) // HOLDS STATE
    val chassis = Chassis(activity) // HOLDS STATE
    val imu = Imu(activity) // HOLDS STATE

    fun start(brainURI: URI){
        val ip = brainURI.uri.split(':')[1]
        val port = brainURI.uri.split(':')[2].toInt()
        channel = ManagedChannelBuilder.forAddress(ip, port).usePlaintext().build()
        cameraSystem.start(channel!!)
        chassis.start(channel!!)
        imu.start(channel!!)
    }

    fun stop(){
        chassis.stop()
        cameraSystem.stop()
        imu.stop()
        channel?.shutdownNow()
    }
}