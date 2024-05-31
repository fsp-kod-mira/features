import grpc
import feature_pb2
import feature_pb2_grpc
from concurrent import futures
import model

grpc_port = '[::]:50051'

class FeatureServicer(feature_pb2_grpc.FeatureServicer):
    
    def Get(self, request, context):
        ams = GetObjects()
        messages = feature_pb2.HibrydFeatureList()
        for s in ams: 
            print(s)
            
            messages.items.append(
                feature_pb2.HibrydFeature(
                    feature_id = s["id"],
                    priority_id = s["priority"]["id"],
                    feature_name = s["name"],
                    priority_name = s["priority"]["name"],
                    coefficient = s["priority"]["coefficient"]
                )
            )
            
        return messages

    
    def AddPriority(self, request, context):
        try:
            model.AddPriority(request.name, request.coefficient)
            priority = GetSession().query(Priority).filter_by(name=request.name).first()
            return feature_pb2.PriorityStruct(id=priority.id, name=priority.name, coefficient=priority.coefficient)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.PriorityStruct()

    def AddFeature(self, request, context):
        try:
            model.AddFeature(request.name, request.priority_id)
            feature = GetSession().query(Feature).filter_by(name=request.name).first()
            return feature_pb2.FeatureStruct(id=feature.id, name=feature.name, priority_id=feature.priority_id)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.FeatureStruct()

    def EditPriority(self, request, context):
        try:
            model.EditPriority(request.id, request.name, request.coefficient)
            return feature_pb2.PriorityStruct(id=request.id, name=request.name, coefficient=request.coefficient)
        except DeleteError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return feature_pb2.PriorityStruct()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.PriorityStruct()

    def EditFeature(self, request, context):
        try:
            model.EditFeature(request.id, request.priority_id, request.name)
            return feature_pb2.FeatureStruct(id=request.id, name=request.name, priority_id=request.priority_id)
        except DeleteError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return feature_pb2.FeatureStruct()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.FeatureStruct()

    def DeletePriority(self, request, context):
        try:
            model.DelPriority(request.id)
            return feature_pb2.Empty()
        except DeleteError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return feature_pb2.Empty()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.Empty()

    def DeleteFeature(self, request, context):
        try:
            model.DelFeature(request.id)
            return feature_pb2.Empty()
        except DeleteError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return feature_pb2.Empty()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.Empty()
 


    def GetFeaturesById(self, request, context):
        try:
            s = model.GetFeatureById(request.id)
            
            return feature_pb2.HibrydFeature(
                    feature_id = s["id"],
                    priority_id = s["priority"]["id"],
                    feature_name = s["name"],
                    priority_name = s["priority"]["name"],
                    coefficient = s["priority"]["coefficient"]
                )
            
        except Exception as e:
            print("Error in GetFeaturesById:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
        
        return templates_pb2.Empty()
        





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_pb2_grpc.add_FeatureServicer_to_server(FeatureServicer(), server)
    server.add_insecure_port(grpc_port)
    server.start()
    server.wait_for_termination()



if __name__ == '__main__':
    print(f"Run server on {grpc_port}")
    serve()
