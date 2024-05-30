import grpc
import feature_pb2
import feature_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = feature_pb2_grpc.FeatureStub(channel)
    
    
    
    response = stub.Get(feature_pb2.Empty())
    
    for feature_item in response.items:
        print(f"Feature ID: {feature_item.feature_id}")
        print(f"Feature Name: {feature_item.priority_name}")
        print(f"Feature Priority ID: {feature_item.coefficient}")
        print()



def add():
    
    channel = grpc.insecure_channel('localhost:50051')
    stub = feature_pb2_grpc.FeatureStub(channel)
    
    res = stub.AddPriority(feature_pb2.PriorityStruct(name="new name 2", coefficient=12))
    
    stub.AddFeature(feature_pb2.FeatureStruct(name="new name of feathure", priority_id=res.id))
    




if __name__ == '__main__':
    #add()
    run()
