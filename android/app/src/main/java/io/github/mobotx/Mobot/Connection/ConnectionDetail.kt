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

import java.util.regex.Pattern

class ConnectionDetail {
    var ip:String? = null
    var port:Int? = null

    fun isNull(): Boolean{
        return ip == null  || port == null
    }

    fun setIpAndPortIfValid(ip: String, port:Int):Boolean{
        val isValid  = isValidIp(ip) && isValidPort(port)
        if (isValid){
            this.ip = ip
            this.port = port
        }
        return isValid
    }

    private fun isValidIp(ip: String):Boolean{
        // Regex for digit from 0 to 255
        val reg0To255 = ("(\\d{1,2}|(0|1)\\" + "d{2}|2[0-4]\\d|25[0-5])")
        // regex 0 To 255 followed by a dot, 4 times repeat
        // validation an IP address.
        val regex = (reg0To255 + "\\."
                + reg0To255 + "\\."
                + reg0To255 + "\\."
                + reg0To255)
        val p = Pattern.compile(regex)
        val m = p.matcher(ip)
        return m.matches()
    }

    private fun isValidPort(port: Int):Boolean{
        return (port >= 0) && (port <= 65535)
    }
}