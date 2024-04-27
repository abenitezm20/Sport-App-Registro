import json
import os
import jwt
import logging

import requests
from src.commands.base_command import BaseCommand
from src.models.deporte import Deporte
from src.models.deporte_deportista import DeporteDeportista
from src.models.db import db_session
from src.errors.errors import ApiError, BadRequest
from flask import request
from sqlalchemy import delete

logger = logging.getLogger(__name__)


class ActualizarDeporteDeportista(BaseCommand):
    def __init__(self, info_deporte_deportista, id_deportista: str):
        super().__init__()
        self.__dict__.update(info_deporte_deportista)
        self.info_deporte_deportista = info_deporte_deportista
        self.id_deportista = id_deportista

    def execute(self):

        #Se eliminan las asignaciones existentes
        dele = delete(DeporteDeportista).where(DeporteDeportista.id_deportista == self.id_deportista)
        db_session.execute(dele)
        db_session.commit()

        logger.info(f'Se asignan nuevos deportes al deportista: {self.id_deportista}')
        #se asignan los nuevos deportes
        for deporte in self.info_deporte_deportista['deportes']:

            if deporte.get('atletismo'):
                if deporte['atletismo'] == 1:
                    deporteBD = db_session.query(Deporte).filter(Deporte.nombre == "Atletismo").first()
                    self.id_deporte = deporteBD.id

                    if self.id_deporte is None:
                        logger.error("Deporte no encontrado")
                        raise BadRequest
                    else:
                        record = DeporteDeportista(id_deporte=self.id_deporte, id_deportista=self.id_deportista)
                        db_session.add(record)
                        db_session.commit()
                else:
                    print("Atletismo no es seleccionado")
            elif deporte.get('ciclismo'):
                if deporte['ciclismo'] == 1:
                    deporteBD = db_session.query(Deporte).filter(Deporte.nombre == "Ciclismo").first()
                    self.id_deporte = deporteBD.id

                    if self.id_deporte is None:
                        logger.error("Deporte no encontrado")
                        raise BadRequest
                    else:
                        record = DeporteDeportista(id_deporte=self.id_deporte, id_deportista=self.id_deportista)
                        db_session.add(record)
                        db_session.commit()
                else:
                    print("Ciclismo no es seleccionado")     
        response = {
            'message': 'success'
        }
        return response
    
    def _getDeporte(self, nombre_deporte: str):
            URL_GESTOR_DEPORTES = os.getenv('URL_GESTOR_DEPORTES', 'http://localhost:3003')
            URL_OBTENER_DEPORTES = URL_GESTOR_DEPORTES + '/gestor-deportes/deportes/obtener_deportes'
            logger.info(f'URL {URL_OBTENER_DEPORTES} nombre_deporte: {nombre_deporte}')

            try:
                response = requests.get(url=URL_OBTENER_DEPORTES)

                if response.json() is not None:
                    data = response.json()
                    for deporte in data:
                        if deporte['nombre'] == nombre_deporte:
                            return deporte['id']
                    return None
                else:
                    return None

            except Exception as e:
                logger.error(f'Error obteniendo deportes {e}')
                raise ApiError
   
   