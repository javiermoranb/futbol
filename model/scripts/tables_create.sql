-- -----------------------------------------------------
-- Schema futbol-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `futbol-db` ;
USE `futbol-db` ;

-- -----------------------------------------------------
-- Table `futbol-db`.`pie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`pie` (
  `id_pie` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(15) NULL,
  PRIMARY KEY (`id_pie`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`posicion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`posicion` (
  `id_posicion` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(30) NULL,
  PRIMARY KEY (`id_posicion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`pais` (
  `id_pais` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL,
  `name` VARCHAR(50) NULL,
  `continente` VARCHAR(45) NULL,
  `codigoISO2` VARCHAR(2) NULL,
  `codigoISO3` VARCHAR(3) NULL,
  PRIMARY KEY (`id_pais`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`somatotipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`somatotipo` (
  `id_somatotipo` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`id_somatotipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`equipo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`equipo` (
  `id_equipo` INT NOT NULL,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`id_equipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`jugador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`jugador` (
  `id_jugador` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(120) NULL,
  `apodo` VARCHAR(120) NULL,
  `anio` INT NULL,
  `id_equipo` INT NOT NULL,
  `numero` INT NULL,
  `id_pie` INT NOT NULL,
  `id_somatotipo` INT NOT NULL,
  `estatura` INT NULL,
  `id_pais` INT NOT NULL,
  `id_pais_nacionalidad` INT NULL,
  `id_posicion1` INT NOT NULL,
  `id_posicion2` INT NULL,
  PRIMARY KEY (`id_jugador`),
  INDEX `fk_jugador_pie1_idx` (`id_pie` ASC),
  INDEX `fk_jugador_posicion1_idx` (`id_posicion1` ASC),
  INDEX `fk_jugador_posicion2_idx` (`id_posicion2` ASC),
  INDEX `fk_jugador_pais1_idx` (`id_pais` ASC),
  INDEX `fk_jugador_pais2_idx` (`id_pais_nacionalidad` ASC),
  INDEX `fk_jugador_somatotipo1_idx` (`id_somatotipo` ASC),
  INDEX `fk_jugador_equipo1_idx` (`id_equipo` ASC),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC),
  UNIQUE INDEX `id_jugador_UNIQUE` (`id_jugador` ASC),
  CONSTRAINT `fk_jugador_pie1`
    FOREIGN KEY (`id_pie`)
    REFERENCES `futbol-db`.`pie` (`id_pie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_posicion1`
    FOREIGN KEY (`id_posicion1`)
    REFERENCES `futbol-db`.`posicion` (`id_posicion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_posicion2`
    FOREIGN KEY (`id_posicion2`)
    REFERENCES `futbol-db`.`posicion` (`id_posicion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_pais1`
    FOREIGN KEY (`id_pais`)
    REFERENCES `futbol-db`.`pais` (`id_pais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_pais2`
    FOREIGN KEY (`id_pais_nacionalidad`)
    REFERENCES `futbol-db`.`pais` (`id_pais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_somatotipo1`
    FOREIGN KEY (`id_somatotipo`)
    REFERENCES `futbol-db`.`somatotipo` (`id_somatotipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_equipo1`
    FOREIGN KEY (`id_equipo`)
    REFERENCES `futbol-db`.`equipo` (`id_equipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`perfil` (
  `id_perfil` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`id_perfil`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`jugador_perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`jugador_perfil` (
  `id_jugador` INT NOT NULL,
  `id_perfil` INT NOT NULL,
  PRIMARY KEY (`id_jugador`, `id_perfil`),
  INDEX `fk_jugador_has_perfil_perfil1_idx` (`id_perfil` ASC),
  INDEX `fk_jugador_has_perfil_jugador_idx` (`id_jugador` ASC),
  CONSTRAINT `fk_jugador_has_perfil_jugador`
    FOREIGN KEY (`id_jugador`)
    REFERENCES `futbol-db`.`jugador` (`id_jugador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jugador_has_perfil_perfil1`
    FOREIGN KEY (`id_perfil`)
    REFERENCES `futbol-db`.`perfil` (`id_perfil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`visualizacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`visualizacion` (
  `id_visualizacion` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(10) NULL,
  PRIMARY KEY (`id_visualizacion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`seguimiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`seguimiento` (
  `id_seguimiento` INT NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`id_seguimiento`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`role` (
  `id_role` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NULL,
  PRIMARY KEY (`id_role`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`user` (
  `id_user` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `email` VARCHAR(50) NULL,
  `password` VARCHAR(120) NULL,
  `id_role` INT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE INDEX `id_user_UNIQUE` (`id_user` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  INDEX `fk_user_role1_idx` (`id_role` ASC),
  CONSTRAINT `fk_user_role1`
    FOREIGN KEY (`id_role`)
    REFERENCES `futbol-db`.`role` (`id_role`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `futbol-db`.`valoracion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `futbol-db`.`valoracion` (
  `id_valoracion` INT NOT NULL AUTO_INCREMENT,
  `id_user` INT NOT NULL,
  `fecha` DATETIME NULL,
  `id_visualizacion` INT NOT NULL,
  `id_equipo` INT NOT NULL,
  `local` INT NOT NULL,
  `visitante` INT NOT NULL,
  `campeonato` VARCHAR(100) NULL,
  `id_seguimiento` INT NOT NULL,
  `descripcion` VARCHAR(1000) NULL,
  `id_jugador` INT NOT NULL,
  `active` VARCHAR(1) NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`id_valoracion`),
  INDEX `fk_valoracion_jugador1_idx` (`id_jugador` ASC),
  INDEX `fk_valoracion_equipo1_idx` (`local` ASC),
  INDEX `fk_valoracion_equipo2_idx` (`visitante` ASC),
  INDEX `fk_valoracion_visualizacion1_idx` (`id_visualizacion` ASC),
  INDEX `fk_valoracion_equipo3_idx` (`id_equipo` ASC),
  INDEX `fk_valoracion_Seguimiento1_idx` (`id_seguimiento` ASC),
  INDEX `fk_valoracion_user1_idx` (`id_user` ASC),
  CONSTRAINT `fk_valoracion_jugador1`
    FOREIGN KEY (`id_jugador`)
    REFERENCES `futbol-db`.`jugador` (`id_jugador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_equipo1`
    FOREIGN KEY (`local`)
    REFERENCES `futbol-db`.`equipo` (`id_equipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_equipo2`
    FOREIGN KEY (`visitante`)
    REFERENCES `futbol-db`.`equipo` (`id_equipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_visualizacion1`
    FOREIGN KEY (`id_visualizacion`)
    REFERENCES `futbol-db`.`visualizacion` (`id_visualizacion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_equipo3`
    FOREIGN KEY (`id_equipo`)
    REFERENCES `futbol-db`.`equipo` (`id_equipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_Seguimiento1`
    FOREIGN KEY (`id_seguimiento`)
    REFERENCES `futbol-db`.`seguimiento` (`id_seguimiento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_valoracion_user1`
    FOREIGN KEY (`id_user`)
    REFERENCES `futbol-db`.`user` (`id_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;