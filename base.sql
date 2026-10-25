-- ========================================================
-- Datos FICTICIOS de ejemplo para Óptica Amaru
-- Si usan mas tablas o modifiquen no weben el codigo porq no serviran muchas funciones
-- ========================================================

-- 1. TIPOS DE LENTE (IDs 1 al 5)
INSERT INTO `opticaapp_tipolente` (`idTipoLente`, `nombre`) VALUES
(1, 'Lentes de lectura'),
(2, 'Lentes para ver de lejos'),
(3, 'Multifocales'),
(4, 'Renovación con receta'),
(5, 'Solo cambio de cristales');

-- 2. ESTADOS (IDs 1 al 6). El campo orden dibuja la línea de tiempo.
INSERT INTO `opticaapp_estado` (`idEstado`, `nombre`, `orden`) VALUES
(1, 'Recibida', 1),
(2, 'En revisión', 2),
(3, 'En taller', 3),
(4, 'Control de calidad', 4),
(5, 'Lista para retiro', 5),
(6, 'Entregada', 6);

-- 3. CLIENTES (IDs 1 al 8)
INSERT INTO `opticaapp_cliente` (`idCliente`, `rut`, `nombre`, `contacto`, `telefono`, `email`, `acepta_datos`) VALUES
(1, '16482915-4', 'Carlos Rojas Muñoz', 'WhatsApp', '+56 9 5551 0101', '', 1),
(2, '12345678-5', 'María Fernanda Soto', 'Llamada', '+56 9 5551 0102', '', 1),
(3, '9876543-3', 'Jorge Pinto Alarcón', 'Correo', '', 'jpinto@correo.cl', 1),
(4, '18765432-7', 'Ana Belén Torres', 'WhatsApp', '+56 9 5551 0104', 'ana.torres@correo.cl', 1),
(5, '14234567-6', 'Luis Cárcamo Díaz', 'Llamada', '+56 9 5551 0105', '', 1),
(6, '20111222-2', 'Valentina Araya Pérez', 'WhatsApp', '+56 9 5551 0106', 'vale.araya@correo.cl', 1),
(7, '11222333-9', 'Héctor Vidal Rivas', 'Llamada', '+56 9 5551 0107', '', 1),
(8, '15333444-7', 'Camila Núñez Leiva', 'Correo', '', 'camila.nunez@correo.cl', 1);

-- 4. SOLICITUDES (IDs 1 al 9). Algunas con la fecha de entrega vencida para que se vea el indicador "con demora".
INSERT INTO `opticaapp_solicitud` (`idSolicitud`, `folio`, `receta`, `filtro_azul`, `indicaciones`, `fecha_creacion`, `fecha_entrega`, `cliente_id`, `estado_id`, `tipo_id`) VALUES
(1, 'AMR-4F7K2Q', '', 1, 'Marco liviano, uso diario en el computador', '2026-10-20 15:10:00', '2026-10-28', 1, 2, 1),
(2, 'AMR-9HX3MD', '', 0, '', '2026-10-15 11:30:00', '2026-10-24', 2, 3, 2),
(3, 'AMR-T6WN8B', '', 0, 'Necesita examen de la vista', '2026-10-21 09:05:00', '2026-10-27', 3, 1, 3),
(4, 'AMR-C2PL5R', '', 1, '', '2026-10-12 17:45:00', '2026-10-23', 4, 5, 4),
(5, 'AMR-E8VZ4K', '', 0, 'Cambiar cristales del marco actual', '2026-10-05 10:20:00', '2026-10-14', 5, 6, 5),
(6, 'AMR-J3QS7Y', '', 1, '', '2026-10-14 12:00:00', '2026-10-22', 6, 4, 1),
(7, 'AMR-M5DA9X', '', 0, '', '2026-10-10 16:40:00', '2026-10-19', 7, 3, 2),
(8, 'AMR-R7BK3N', '', 0, 'Quiere el mismo marco', '2026-10-21 08:15:00', '2026-10-29', 8, 2, 4),
(9, 'AMR-Y4HC6T', '', 0, '', '2026-09-10 10:00:00', '2026-09-17', 1, 6, 5);
