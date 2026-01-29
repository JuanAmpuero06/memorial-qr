# Usamos Node.js versión ligera
FROM node:22-alpine

WORKDIR /app

# Copiamos los archivos de dependencias
COPY package.json ./

# Instalamos (dentro del contenedor)
RUN npm install

# Copiamos el resto del código
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Comando para iniciar en modo desarrollo
# --host es VITAL para que Docker pueda exponer el puerto
CMD ["npm", "run", "dev", "--", "--host"]