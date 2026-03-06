import requests

BASE_URL = "https://reqres.in/api/tareas"  #

print("GET - Lista de tareas")
response = requests.get(BASE_URL)
print("Código de estado:", response.status_code)
print(response.json())
print("\n")

print("POST - Crear nueva tarea")
nueva_tarea = {
    "titulo": "Estudiar HTTP",
    "estado": "pendiente"
}
response = requests.post(BASE_URL, json=nueva_tarea)
print("Código de estado:", response.status_code)
print(response.json())
print("\n")

print("PUT - Actualizar tarea")

actualizacion = {
    "estado": "completada"
}
response = requests.put(BASE_URL + "/2", json=actualizacion)
print("Código de estado:", response.status_code)
print(response.json())
print("\n")

print("DELETE - Eliminar tarea")

response = requests.delete(BASE_URL + "/1")
print("Código de estado:", response.status_code)  
print("Contenido:", response.text)  
