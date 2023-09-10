import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";

import { Context } from "../store/appContext";

export const MetodoPago = () => {
    const { store, actions } = useContext(Context);

    return (
        <div className="">
            <div className="text-center m-4">
                <h1>Métodos de pago</h1>
            </div>
            <div className="d-flex justify-content-center">
                <img src="https://utilitario.leon.cl/prod/img/web/FormasDePago.png" alt="Descripción de la imagen" />
            </div>
            <div className="mx-5">
                <p>Salvo que se señale un Medio de Pago diferente para casos u ofertas específicas, los productos y servicios informados en el sitio Web sólo podrán ser pagados por los siguientes medios:</p>
                <p>1.Tarjeta de Débito Bancarias acogidas al sistema Redcompra: esto es Tarjetas emitidas en Chile por Bancos Nacionales, que se encuentren afiliadas a TransBank.</p>
                <p>2.Tarjetas de Crédito Bancarias: esto es tarjetas emitidas en Chile o en el extranjero por Bancos Nacionales o Internacionales que se encuentren afiliadas a TransBank.</p>
                <p>3.Transferencias bancarias.</p>
                <p>4.Efectivo</p>
                <p>5.BitCoins</p>
            </div>
        </div >
    );
};