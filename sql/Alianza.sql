-- MySQL dump 10.13  Distrib 5.1.61, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Alianza
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.11.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alumnos`
--

DROP TABLE IF EXISTS `alumnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alumnos` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `cliente_id` bigint(20) DEFAULT NULL,
  `curso_id` bigint(20) DEFAULT NULL,
  `tipo_pago_id` bigint(20) DEFAULT NULL,
  `cuota` double(255,8) DEFAULT NULL,
  `pago` tinyint(4) DEFAULT NULL,
  `finalizado` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1856 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `balcom`
--

DROP TABLE IF EXISTS `balcom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `balcom` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item` varchar(45) NOT NULL,
  `enero` decimal(20,2) DEFAULT '0.00',
  `febrero` decimal(20,2) DEFAULT '0.00',
  `marzo` decimal(20,2) DEFAULT '0.00',
  `abril` decimal(20,2) DEFAULT '0.00',
  `mayo` decimal(20,2) DEFAULT '0.00',
  `junio` decimal(20,2) DEFAULT '0.00',
  `julio` decimal(20,2) DEFAULT '0.00',
  `agosto` decimal(20,2) DEFAULT '0.00',
  `setiembre` decimal(20,2) DEFAULT '0.00',
  `octubre` decimal(20,2) DEFAULT '0.00',
  `noviembre` decimal(20,2) DEFAULT '0.00',
  `diciembre` decimal(20,2) DEFAULT '0.00',
  `ano` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=latin1 ROW_FORMAT=FIXED COMMENT='Balance comparativo';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bie_cam`
--

DROP TABLE IF EXISTS `bie_cam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bie_cam` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) DEFAULT NULL,
  `precio` decimal(20,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=60 DEFAULT CHARSET=latin1 COMMENT='Bienes de cambio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bol_cont`
--

DROP TABLE IF EXISTS `bol_cont`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bol_cont` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caja_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `efectivo` decimal(10,0) DEFAULT NULL,
  `cheques` decimal(10,0) DEFAULT NULL,
  `vouchers` decimal(10,0) DEFAULT NULL,
  `otros` decimal(10,0) DEFAULT NULL,
  `total` double DEFAULT NULL,
  `flag` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11221 DEFAULT CHARSET=latin1 COMMENT='Boletas contado';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bol_det`
--

DROP TABLE IF EXISTS `bol_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bol_det` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bol_cont_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `detalle` varchar(50) DEFAULT NULL,
  `unitario` decimal(10,0) DEFAULT NULL,
  `total` decimal(10,0) DEFAULT NULL,
  `rubro` int(11) DEFAULT NULL,
  `extra_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13192 DEFAULT CHARSET=latin1 COMMENT='Detalle de boletas contado';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cajas`
--

DROP TABLE IF EXISTS `cajas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cajas` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `apertura` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `a_efectivo` double(255,8) DEFAULT NULL,
  `a_cheques` double(255,8) DEFAULT NULL,
  `a_vouchers` double(255,8) DEFAULT NULL,
  `a_otros` double(255,8) DEFAULT NULL,
  `cierre` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `c_efectivo` double(255,8) DEFAULT NULL,
  `c_cheques` double(255,8) DEFAULT NULL,
  `c_vouchers` double(255,8) DEFAULT NULL,
  `c_otros` double(255,8) DEFAULT NULL,
  `deposito_id` int(11) DEFAULT NULL,
  `cerrado` tinyint(1) DEFAULT NULL,
  `usuario` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3252 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cat_clientes`
--

DROP TABLE IF EXISTS `cat_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat_clientes` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `categoria` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cat_empleados`
--

DROP TABLE IF EXISTS `cat_empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat_empleados` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `categoria` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `nombre` char(50) DEFAULT NULL,
  `direccion` char(50) DEFAULT NULL,
  `telefono` char(50) DEFAULT NULL,
  `email` char(50) DEFAULT NULL,
  `ultimo_contacto` date DEFAULT NULL,
  `saldo` double(255,8) DEFAULT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `ci` char(50) DEFAULT NULL,
  `notas` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1658 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clientesb`
--

DROP TABLE IF EXISTS `clientesb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientesb` (
  `nombre` char(50) NOT NULL,
  `telefono` char(50) DEFAULT NULL,
  `ci` char(50) DEFAULT NULL,
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `correo` char(50) DEFAULT NULL,
  `notas` longtext,
  `categoria_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=284 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `codigoss`
--

DROP TABLE IF EXISTS `codigoss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codigoss` (
  `id` bigint(10) NOT NULL,
  `codigo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Códigos de Seguro de Salud';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comprobantes`
--

DROP TABLE IF EXISTS `comprobantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comprobantes` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `definicion` char(50) DEFAULT NULL,
  `origen_id` bigint(20) DEFAULT NULL,
  `destino_id` bigint(20) DEFAULT NULL,
  `tipo_comprobante_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `conciliacion`
--

DROP TABLE IF EXISTS `conciliacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conciliacion` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `id_id` bigint(1) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `detalle` char(50) DEFAULT NULL,
  `cuenta_id` bigint(20) DEFAULT NULL,
  `debe` double(255,8) DEFAULT NULL,
  `haber` double(255,8) DEFAULT NULL,
  `documento_id` bigint(20) DEFAULT NULL,
  `check` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=360 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado`
--

DROP TABLE IF EXISTS `consolidado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado2003`
--

DROP TABLE IF EXISTS `consolidado2003`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado2003` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado2004`
--

DROP TABLE IF EXISTS `consolidado2004`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado2004` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado2005`
--

DROP TABLE IF EXISTS `consolidado2005`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado2005` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `srub` varchar(6) NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado2006`
--

DROP TABLE IF EXISTS `consolidado2006`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado2006` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `srub` varchar(6) NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consolidado2007`
--

DROP TABLE IF EXISTS `consolidado2007`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consolidado2007` (
  `rubro` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `enero` double NOT NULL,
  `febrero` double NOT NULL,
  `marzo` double NOT NULL,
  `abril` double NOT NULL,
  `mayo` double NOT NULL,
  `junio` double NOT NULL,
  `julio` double NOT NULL,
  `agosto` double NOT NULL,
  `setiembre` double NOT NULL,
  `octubre` double NOT NULL,
  `noviembre` double NOT NULL,
  `diciembre` double NOT NULL,
  `srub` varchar(6) NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cta_clientes`
--

DROP TABLE IF EXISTS `cta_clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cta_clientes` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `cliente_id` bigint(20) DEFAULT NULL,
  `grupo_id` bigint(20) DEFAULT NULL,
  `concepto` char(50) DEFAULT NULL,
  `debe` double(255,8) DEFAULT NULL,
  `haber` double(255,8) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9415 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cta_empleados`
--

DROP TABLE IF EXISTS `cta_empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cta_empleados` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `empleado_id` bigint(20) NOT NULL,
  `fecha` date DEFAULT NULL,
  `detalle` varchar(50) DEFAULT NULL,
  `debe` decimal(20,2) DEFAULT NULL,
  `haber` decimal(20,2) DEFAULT NULL,
  `extra_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1 COMMENT='Cuenta corriente de empleados';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuentas`
--

DROP TABLE IF EXISTS `cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuentas` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `rubro` bigint(20) NOT NULL,
  `nombre` char(50) DEFAULT NULL,
  `tipo_id` bigint(20) DEFAULT NULL,
  `nivel` int(11) DEFAULT NULL,
  `fee` decimal(5,3) DEFAULT NULL,
  `impuestos` decimal(5,3) DEFAULT NULL,
  `auxiliar` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=248 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cursos`
--

DROP TABLE IF EXISTS `cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cursos` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `curso` char(50) NOT NULL DEFAULT 'nombre',
  `empleado_id` bigint(20) DEFAULT NULL,
  `deposito_id` bigint(20) DEFAULT NULL,
  `tipo_id` int(11) DEFAULT '0',
  `dias` char(5) DEFAULT '',
  `horas` char(11) DEFAULT '',
  `notas` text,
  `finalizado` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=279 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `depositos`
--

DROP TABLE IF EXISTS `depositos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `depositos` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `deposito` char(50) DEFAULT NULL,
  `codigo` char(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `desarrollo`
--

DROP TABLE IF EXISTS `desarrollo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `desarrollo` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario` char(20) DEFAULT NULL,
  `cambios` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `detalle` char(50) DEFAULT NULL,
  `estado` bigint(20) DEFAULT NULL,
  `notas` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=272 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `det_liquidacion`
--

DROP TABLE IF EXISTS `det_liquidacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `det_liquidacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `liquidacion_id` bigint(20) NOT NULL,
  `empleado_id` bigint(20) NOT NULL,
  `horas_sem` decimal(20,2) NOT NULL,
  `horas_reloj` decimal(20,2) NOT NULL,
  `extras` decimal(20,2) DEFAULT NULL,
  `sueldo` decimal(20,2) NOT NULL,
  `sueldo_reloj` decimal(20,2) NOT NULL,
  `nominal` decimal(20,2) NOT NULL,
  `aguinaldo` decimal(20,2) NOT NULL,
  `licencia` decimal(20,2) NOT NULL,
  `vacacional` decimal(20,2) NOT NULL,
  `antiguedad` decimal(20,2) NOT NULL,
  `bps` decimal(20,2) NOT NULL,
  `disse` decimal(20,2) NOT NULL,
  `frl` decimal(20,2) NOT NULL,
  `irpf` decimal(20,2) NOT NULL,
  `adelantos` decimal(20,2) NOT NULL,
  `liquido` decimal(20,2) NOT NULL,
  `cjp` decimal(20,2) DEFAULT NULL,
  `valor_hs` decimal(20,2) DEFAULT '0.00',
  `valor_hr` decimal(20,2) DEFAULT '0.00',
  `ficto_semanal` decimal(20,2) DEFAULT '0.00',
  `porcentaje_fonasa` decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1928 DEFAULT CHARSET=latin1 COMMENT='detalle de liquidacion de sueldos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deudores`
--

DROP TABLE IF EXISTS `deudores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deudores` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cliente_id` bigint(20) DEFAULT NULL,
  `curso_id` bigint(20) DEFAULT NULL,
  `ultima` date DEFAULT NULL,
  `extra` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1082 DEFAULT CHARSET=latin1 COMMENT='tabla temporaria de deudores';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `docentes`
--

DROP TABLE IF EXISTS `docentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docentes` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `nombre` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empleados` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `nombre` char(50) DEFAULT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `ci` char(50) DEFAULT NULL,
  `direccion` char(50) DEFAULT NULL,
  `telefono` char(50) DEFAULT NULL,
  `email` char(50) DEFAULT NULL,
  `ingreso` date DEFAULT NULL,
  `notas` longtext,
  `sexo` char(10) DEFAULT NULL,
  `f_nac` date DEFAULT NULL,
  `e_civil` char(10) DEFAULT NULL,
  `hijos` bigint(20) NOT NULL,
  `emni` tinyint(1) NOT NULL,
  `codigoss` bigint(10) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `existencias`
--

DROP TABLE IF EXISTS `existencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `existencias` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `deposito_id` bigint(20) DEFAULT NULL,
  `bie_cam_id` bigint(20) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1145 DEFAULT CHARSET=latin1 COMMENT='Control de Stock';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inf_fin`
--

DROP TABLE IF EXISTS `inf_fin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inf_fin` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `bancos` text NOT NULL,
  `bancosb0` text NOT NULL,
  `egresos` text NOT NULL,
  `ingresos` text NOT NULL,
  `ganancia` text NOT NULL,
  `conclusion` text NOT NULL,
  `recomendaciones` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COMMENT='Informe financiero';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `deposito_id` int(11) DEFAULT NULL,
  `compra` date DEFAULT NULL,
  `costo` decimal(10,0) DEFAULT NULL,
  `vida` int(11) DEFAULT NULL,
  `residual` decimal(10,0) DEFAULT NULL,
  `metodo` varchar(50) DEFAULT NULL,
  `revaluacion` decimal(10,0) DEFAULT NULL,
  `fecha_rev` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Registro de bienes de uso';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `liquidacion`
--

DROP TABLE IF EXISTS `liquidacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `liquidacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `variables_id` bigint(20) NOT NULL,
  `salario_id` bigint(20) NOT NULL,
  `corresponde` varchar(50) DEFAULT NULL,
  `liquido` decimal(20,2) NOT NULL,
  `BPS` decimal(20,2) NOT NULL,
  `DGI` decimal(20,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=latin1 COMMENT='Master Liquidación de sueldos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `llamadas`
--

DROP TABLE IF EXISTS `llamadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `llamadas` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `cliente_id` bigint(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `notas` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=331 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mov_caja`
--

DROP TABLE IF EXISTS `mov_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mov_caja` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `caja_id` bigint(20) DEFAULT NULL,
  `tiempo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `detalle` char(50) CHARACTER SET latin1 DEFAULT NULL,
  `efectivo` double(255,8) DEFAULT NULL,
  `cheques` double(255,8) DEFAULT NULL,
  `vouchers` double(255,8) DEFAULT NULL,
  `otros` double(255,8) DEFAULT NULL,
  `contabilizado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22025 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `producto` varchar(50) DEFAULT NULL,
  `rubro` int(11) DEFAULT NULL,
  `precio` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='Lista de productos para boletas';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proveedores` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `proveedor` char(50) DEFAULT NULL,
  `cuenta_id` bigint(20) DEFAULT NULL,
  `telefono` char(50) DEFAULT NULL,
  `direccion` char(50) DEFAULT NULL,
  `email` char(50) DEFAULT NULL,
  `ruc` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registro`
--

DROP TABLE IF EXISTS `registro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registro` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `usuario` char(20) NOT NULL,
  `entrada` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6361 DEFAULT CHARSET=latin1 COMMENT='Registro de entradas al sistema';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `salario`
--

DROP TABLE IF EXISTS `salario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salario` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `cat_empleado_id` bigint(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora_reloj` decimal(20,2) DEFAULT NULL,
  `hora_semanal` decimal(20,2) DEFAULT NULL,
  `mensual` decimal(20,2) DEFAULT NULL,
  `ficto_semanal` decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=106 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_comprobante`
--

DROP TABLE IF EXISTS `tipo_comprobante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_comprobante` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `tipo` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_cuenta`
--

DROP TABLE IF EXISTS `tipo_cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cuenta` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `tipo` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_curso`
--

DROP TABLE IF EXISTS `tipo_curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_curso` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `tipo` char(50) DEFAULT NULL,
  `codigo` char(4) DEFAULT NULL,
  `rubro` int(11) DEFAULT '0',
  `duracion` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=latin1 COMMENT='Tabla con tipos posibles de cursos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_pago`
--

DROP TABLE IF EXISTS `tipo_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_pago` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `tipo` char(50) DEFAULT NULL,
  `descuento` double(255,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transacciones` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `detalle` char(50) DEFAULT NULL,
  `cuenta_id` bigint(20) DEFAULT NULL,
  `debe` double(255,8) DEFAULT NULL,
  `haber` double(255,8) DEFAULT NULL,
  `documento_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11985 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `usuario` char(20) NOT NULL,
  `creacion` date NOT NULL,
  `clave` char(255) NOT NULL,
  `nombre` char(50) DEFAULT NULL,
  `nivel` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `deposito_id` bigint(10) DEFAULT NULL,
  PRIMARY KEY (`usuario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `variables`
--

DROP TABLE IF EXISTS `variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variables` (
  `id` bigint(1) NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `sm` decimal(20,2) DEFAULT NULL,
  `bcp` decimal(20,2) DEFAULT NULL,
  `bps` decimal(20,2) DEFAULT NULL,
  `disse` decimal(20,2) DEFAULT NULL,
  `frl` decimal(20,3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-01 14:10:48
