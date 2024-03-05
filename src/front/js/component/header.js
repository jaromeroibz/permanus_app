import React from "react";
import permanusImageUrl from "../../img/permanus.png";
import { Link } from "react-router-dom";
import { faSearch } from "@fortawesome/free-solid-svg-icons";


export const Header = () =>{
    return(
        <>
        <div className="announcement-bar">
            <p>Hecho en Costa Rica • Envíos gratis $75+ • Garantía de por vida</p>
        </div>
        <Link to="/">
            <div className="header">
                <div className="search-box">
                    <form class="search-form" action="/buscar" method="get" role="search">
                        <input type="search" id="search" name="search" placeholder="Buscar"></input>
                        <button>
                            <span class="material-symbols-outlined">search</span>
                        </button>
                    </form>
                </div>
                <img className= "permanus-img img_fluid" src={permanusImageUrl} />
            </div>
        </Link>
        </>

    )
}