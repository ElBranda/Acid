# ACID
Generador de Libro de Sueldos Digital de ARCA. Reversión del antiguo sistema `TProject` por cambio en el formato de los archivos actuales de ARCA.

## Sistema
### Backend
Internamente está separado en tres partes:

1. **Lector**: Obtener los datos.
2. **Sistematizador**: Procesar los datos.
3. **Documentador**: Escribir los datos.

Cada uno se encarga de hacer lo que su nombre indica que hace. Una parte jamás hará lo que otra parte hace.

### Frontend
Idea inicial: usar el módulo de Qt para Python.

{ Actualmente en desarrollo }

## Manejo de entrada y salida
### Entrada
Los datos de origen no tienen un formato generalizado. Se debe de tener mucho cuidado en cómo se toman los datos de un específico cliente, puesto que puede no resultar igual para otro diferente.

### Salida
La salida está prevista ser un archivo TXT con el siguiente formato para el nombre: `LSD[mes][año].txt`

## Cosas a tener en cuenta
Los resultados TXT deben tener un formato específico, bien documentado en los instructivos Excel de Arca. Si algún formato falla, por pequeño que sea, todo el archivo es rechazado.

## Firma
Desarrollador: Martín Brandalisi

Hecho en: Junio de 2026