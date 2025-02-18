# Costes de Desarrollo - Proyecto FisioFind

## Equipo
El equipo de desarrollo de FisioFind está compuesto por **17 personas**, distribuidas de la siguiente manera:

- **5 Analistas**
- **1 Project Manager (PM)**
- **11 Desarrolladores Fullstack**

Estos roles asumirán los costes de desarrollo que deberán rentabilizarse a largo plazo para lograr el retorno de inversión.

---

## Horas de Trabajo Mensuales
Antes de rentabilizar la aplicación, se estima el siguiente número de horas de trabajo por mes:

- **Febrero, Abril y Mayo:** 30 horas + **20% de incremento** → **36 horas**
- **Marzo:** 40 horas + **20% de incremento** → **48 horas**

### Coste por Hora según Perfil

- **Desarrollador:** 27€/hora
- **Analista:** 30,82€/hora
- **Project Manager:** 37,25€/hora

El cálculo del coste mensual se realiza multiplicando las horas por el coste horario de cada perfil.

---

## Costes de Hardware

Se estima que la **vida útil media de un equipo es de 3 años**, lo que implica que cada año se debe renovar **1/3 de los equipos**. El coste medio de un equipo es **800€**, por lo que:

- Renovación de equipos: **5.5 equipos/año x 800€ = 4400€**
- Se aplica un **20% de contingencia**: **4400€ × 1.2 = 5280€/año**
- Coste mensual de hardware: **5280€/12 = 440€/mes**

Este coste se sumará a los costes de desarrollo y será constante en el tiempo.

---

## Costes de Licencias y Herramientas

### GitHub Enterprise
Se utilizará **GitHub Enterprise** para la gestión del código del equipo. El coste es de:

- **20,04€ por miembro del equipo**
- Total: **20,04€ x 17 = 340,68€/mes**

### Entorno de Desarrollo y Pre-producción
Para entornos de prueba y pre-producción se estima un coste fijo de **20€/mes**.

---

## Cálculo de Costes Mensuales

Se suman todos los costes fijos mensuales:

| Concepto | Coste Mensual |
|----------|--------------|
| Coste de desarrollo (según horas y roles) | **A calcular** |
| Coste de hardware | **440€** |
| GitHub Enterprise | **340,68€** |
| Entorno de pre-producción | **20€** |
| **Subtotal** | **A calcular** |
| **Contingencia (10%)** | **+10% sobre subtotal** |
| **Total Coste de Desarrollo** | **A calcular** |

El coste de desarrollo mensual variará según el mes, ya que depende de las horas de trabajo asignadas. Una vez sumados todos los costes mensuales, se aplicará un **10% de margen de contingencia**.

---

## Coste Total del Desarrollo

Para calcular el coste total del desarrollo, se sumarán los costes mensuales hasta el mes de mayo (previo al inicio de producción en junio).

---

En la siguiente sección se detallarán los **costes de producción**, que comenzarán a partir de junio.

# Costes de Desarrollo y Producción - Proyecto FisioFind

## Equipo
El equipo de desarrollo de FisioFind está compuesto por **17 personas**, distribuidas de la siguiente manera:

- **5 Analistas**
- **1 Project Manager (PM)**
- **11 Desarrolladores Fullstack**

Estos roles asumirán los costes de desarrollo que deberán rentabilizarse a largo plazo para lograr el retorno de inversión.

---

## Horas de Trabajo Mensuales
Antes de rentabilizar la aplicación, se estima el siguiente número de horas de trabajo por mes:

- **Febrero, Abril y Mayo:** 30 horas + **20% de incremento** → **36 horas**
- **Marzo:** 40 horas + **20% de incremento** → **48 horas**

### Coste por Hora según Perfil

- **Desarrollador:** 27€/hora
- **Analista:** 30,82€/hora
- **Project Manager:** 37,25€/hora

El cálculo del coste mensual se realiza multiplicando las horas por el coste horario de cada perfil.

---

## Costes de Hardware

Se estima que la **vida útil media de un equipo es de 3 años**, lo que implica que cada año se debe renovar **1/3 de los equipos**. El coste medio de un equipo es **800€**, por lo que:

- Renovación de equipos: **5.5 equipos/año x 800€ = 4400€**
- Se aplica un **20% de contingencia**: **4400€ × 1.2 = 5280€/año**
- Coste mensual de hardware: **5280€/12 = 440€/mes**

Este coste se sumará a los costes de desarrollo y será constante en el tiempo.

---

## Costes de Licencias y Herramientas

### GitHub Enterprise
Se utilizará **GitHub Enterprise** para la gestión del código del equipo. El coste es de:

- **20,04€ por miembro del equipo**
- Total: **20,04€ x 17 = 340,68€/mes**

### Entorno de Desarrollo y Pre-producción
Para entornos de prueba y pre-producción se estima un coste fijo de **20€/mes**.

---

## Costes de Producción (Desde Junio)

A partir de junio, los costes de producción incluirán los siguientes elementos:


### Soporte Chatbot
Para soporte técnico de primer nivel, se estima el **plan más caro**, con un coste de **425,51€/mes**.

### Despliegue y Transferencia de Datos

- **Despliegue:** Se incrementa de 20€ a **60€/mes**.
- **Transferencia de datos en Google Cloud:** Dependiendo del uso de videos y documentos. **(Se calcula en base a los usuarios activos).**

### APIs Necesarias

- Verificación de DNI
- Mapa
- SMS
- Videollamada

Para cubrir el peor escenario posible, se estima un **coste entre 1000€ y 2000€ anuales** por el uso de estas APIs.

---

## Costes de Mantenimiento

### Mantenimiento Adaptativo
Se realizarán **revisiones trimestrales**, asignando a un desarrollador **2 jornadas laborables** para verificar que la aplicación no presenta brechas debido a actualizaciones. Este coste se puede dividir entre 12 meses o concentrarlo en los meses correspondientes.

### Mantenimiento Correctivo
El chatbot atenderá la mayoría de las incidencias, pero aquellas que requieran intervención de nivel superior generarán costes adicionales.

- Se estima **10 incidencias/mes** en el peor de los casos.
- Se asume que cada incidencia requerirá **1 hora de resolución**.
- Se usará la tarifa de **27€/hora** (salario de desarrollador).
- **Coste mensual estimado: 10 x 27€ = 270€/mes**.

Este parámetro podrá modificarse según la evolución de la aplicación.

---

## Estimación de Retorno de Inversión

Para calcular el retorno de inversión inicial:

- Se estima el registro de **100 fisioterapeutas** en el primer mes.
- Planes de suscripción:
  - **18,99€ estándar**
  - **23,99€ PRO (estimando que no superará el 20%)**

El cálculo del retorno será dinámico, permitiendo modificar los parámetros en la aplicación de análisis de costes.

---

Este documento servirá como base para que el equipo pueda modificar los parámetros y actualizar los costes de manera flexible.
