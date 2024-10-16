-- database/create_db.sql

CREATE DATABASE IF NOT EXISTS db_academica;

USE db_academica;

CREATE TABLE IF NOT EXISTS usuarios (
  idUsuario INT(10) AUTO_INCREMENT PRIMARY KEY,
  usuario CHAR(35) NOT NULL,
  clave CHAR(35) NOT NULL,
  nombre CHAR(85),
  direccion CHAR(100),
  telefono CHAR(9)
);
