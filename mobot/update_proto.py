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
