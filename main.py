import grpc
import feature_pb2
import feature_pb2_grpc
from concurrent import futures
from model import *

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
            AddPriority(request.name, request.coefficient)
            priority = GetSession().query(Priority).filter_by(name=request.name).first()
            return feature_pb2.PriorityStruct(id=priority.id, name=priority.name, coefficient=priority.coefficient)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.PriorityStruct()

    def AddFeature(self, request, context):
        try:
            AddFeature(request.name, request.priority_id)
            feature = GetSession().query(Feature).filter_by(name=request.name).first()
            return feature_pb2.FeatureStruct(id=feature.id, name=feature.name, priority_id=feature.priority_id)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.FeatureStruct()

    def EditPriority(self, request, context):
        try:
            EditPriority(request.id, request.name, request.coefficient)
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
            EditFeature(request.id, request.priority_id, request.name)
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
            DelPriority(request.id)
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
            DelFeature(request.id)
            return feature_pb2.Empty()
        except DeleteError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return feature_pb2.Empty()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.Empty()
 




   


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_pb2_grpc.add_FeatureServicer_to_server(FeatureServicer(), server)
    server.add_insecure_port(grpc_port)
    server.start()
    print("Сервер запущен...")
    server.wait_for_termination()




def main():
    AddPriority(name="High Priority", coefficient=1.5)
    print("Добавлен приоритет: High Priority")

    priority_id = GetSession().query(Priority).filter_by(name="High Priority").first().id
    AddFeature(name="New Feature 1", priority_id=priority_id)
    print("Добавлена фича: New Feature 1")

    objects = GetObjects()
    print("Все объекты:")
    for obj in objects:
        print(obj)

    EditPriority(priority_id, name="Updated Priority", coefficient=2.0)
    print("Приоритет обновлен: Updated Priority")

    feature_id = GetSession().query(Feature).filter_by(name="New Feature 1").first().id
    EditFeature(feature_id, priority_id, name="Updated Feature 1")
    print("Фича обновлена: Updated Feature 1")

    DelFeature(feature_id)
    print(f"Фича с ID {feature_id} удалена")

    try:
        DelPriority(priority_id)
        print(f"Приоритет с ID {priority_id} удален")
    except DeleteError as e:
        print(e)

#if __name__ == "__main__":
#    main()

if __name__ == '__main__':
    print(f"Run server on {grpc_port}")
    serve()
