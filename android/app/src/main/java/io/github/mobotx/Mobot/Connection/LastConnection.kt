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

package io.github.mobotx.Mobot.Connection

import android.content.Context
import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatActivity
import io.github.mobotx.Mobot.Connection.ConnectionDetail

class LastConnection(private val activity: AppCompatActivity) {

    private val sharedPref: SharedPreferences = activity.getPreferences(Context.MODE_PRIVATE)

    fun loadConnectionDetail(): ConnectionDetail {
        val ip = sharedPref.getString("ip", "null")
        val port = sharedPref.getInt("port", -1)
        val connectionDetail = ConnectionDetail()
        if (ip != "null" && port != -1){
            connectionDetail.setIpAndPortIfValid(ip!! , port)
        }
        return connectionDetail
    }

    fun saveConnectionDetail(connectionDetail: ConnectionDetail){
        if (!connectionDetail.isNull()){
            Thread(Runnable {
                with(sharedPref.edit()) {
                    putString("ip", connectionDetail.ip)
                    putInt("port", connectionDetail.port!!)
                    apply()
                }
            }).start()
        }
    }
}