#!/bin/bash

# Subir todo el contenido del repositorio actual a GitHub

echo "⏳ Verificando archivos modificados o nuevos..."
git status

echo ""
echo "➕ Agregando todos los archivos..."
git add .

echo ""
echo "📝 Confirmando cambios con mensaje genérico..."
git commit -m "Sync: subir todos los archivos generados por Codex"

echo ""
echo "📤 Subiendo al repositorio remoto..."
git push

echo ""
echo "✅ Proceso terminado. Revisa en GitHub si todo fue sincronizado."
