if [ "$1" != "" ]; then
    FILE="$1"
else
    read -p 'Input filename without .proto: ' FILE
fi

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $FILE.proto

sed -i "s/import ${FILE}_pb2/from . import ${FILE}_pb2/" "${FILE}_pb2_grpc.py"
