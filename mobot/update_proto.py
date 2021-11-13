# MIT License
#
# Copyright (c) 2021 Mobotx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

proto_src = "../proto"
proto_dist = "./src/mobot/_proto"

protos = [file for file in os.listdir(proto_src) if file.split('.')[-1] == "proto"]

for proto in protos:
    os.system(f"python3 -m grpc_tools.protoc -I{proto_src} --python_out={proto_dist} --grpc_python_out={proto_dist} {proto}")

protos_pb2 = [f"{proto.split('.')[0]}_pb2" for proto in protos]
protos_pb2_grpc = [f"{proto.split('.')[0]}_pb2_grpc" for proto in protos]

for file in protos_pb2 + protos_pb2_grpc:
    fd = open(proto_dist + f"/{file}.py" , "r")
    lines = fd.read().splitlines()
    for line_no, line in enumerate(lines):
        words = line.split(' ')
        if words[0] == "import":
            if words[1] in protos_pb2 + protos_pb2_grpc:
                words[0] = "from . import"
                line = ' '.join(words)
                lines[line_no] = line
    fd.close()
    fd = open(proto_dist + f"/{file}.py" , "w")
    fd.write("\n".join(lines))
    fd.close()
