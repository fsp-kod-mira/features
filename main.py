import grpc
import feature_pb2
import feature_pb2_grpc
from concurrent import futures
import model
import logging
import os
from model import DeleteError, Priority, Feature
from sqlalchemy.exc import IntegrityError
from grpc_reflection.v1alpha import reflection


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


grpc_port = os.environ.get('GRPC_IPPORT')
if grpc_port == None:
    grpc_port = '0.0.0.0:50052'


class FeatureServicer(feature_pb2_grpc.FeatureServicer):
    
    def Get(self, request, context):
        logger.info("Get request")
        ams = model.GetObjects()
        messages = feature_pb2.HibrydFeatureList()
        for s in ams: 
            
            messages.items.append(
                feature_pb2.HibrydFeature(
                    feature_id    = s["id"],
                    priority_id   = s["priority"]["id"],
                    feature_name  = s["name"],
                    priority_name = s["priority"]["name"],
                    coefficient   = s["priority"]["coefficient"]
                )
            )
            
        return messages

    


    def AddPriority(self, request, context):
        logger.info("AddPriority request")
        try:
            model.AddPriority(request.name, request.coefficient)
            priority = model.GetSession().query(model.Priority).filter_by(name=request.name).first()
            return feature_pb2.IdStruct(id=priority.id)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return feature_pb2.Empty()




    def AddFeature(self, request, context):
        logger.info("AddFeature request")
        try:
            feature = model.GetFeatureByName(request.name)

            if feature:
                
                #context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                return feature_pb2.FeatureStruct(id=feature.id, name=feature.name, priority_id=feature.priority_id)
            
            else:

                model.AddFeature(request.name, request.priority_id)
                feature = model.GetSession().query(model.Feature).filter_by(name=request.name).first()
                return feature_pb2.FeatureStruct(id=feature.id, name=feature.name, priority_id=feature.priority_id)
        
        except Exception as e:

            #context.set_details(e)
            context.set_code(grpc.StatusCode.INTERNAL)

            print(e)           




    def GetFeaturesByName(self, request, context):
        logger.info("AddFeature request")
        try:
            
            feature = model.GetFeatureByName(request.name)
         
            if feature:
                #context.set_details(str(e))
                #context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                return feature_pb2.FeatureStruct(id=feature.id, name=feature.name, priority_id=feature.priority_id)
            
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)

        except Exception as e:

            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            

# get feature by name






    def EditPriority(self, request, context):
        logger.info("EditPriority request")
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
        logger.info("EditFeature request")
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
        logger.info("DeletePriority request")
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
        logger.info("DeleteFeature request")
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
        logger.info("GetFeaturesById request")
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
        
        return feature_pb2.Empty()
        





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_pb2_grpc.add_FeatureServicer_to_server(FeatureServicer(), server)
    SERVICE_NAMES = (
            feature_pb2.DESCRIPTOR.services_by_name['Feature'].full_name,
            reflection.SERVICE_NAME,
        )

    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(grpc_port)
    server.start()
    server.wait_for_termination()



if __name__ == '__main__':
    logger.info(f"Run server on {grpc_port}")
    serve()
