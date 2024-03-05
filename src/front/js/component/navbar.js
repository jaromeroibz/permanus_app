import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
	return (
		<>
		<nav className="nav">
			<div className="container">
				<Link className="nav-content" to="/brazaletes">Brazaletes
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/anillos">Anillos
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/collares">Collares
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/tobilleras">Tobilleras
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/piercings">Piercing/Simuladores
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/colecciones">Colecciones
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
				<Link className="nav-content" to="/edicionlimitada">Edicion Limitada
				<span class="material-symbols-outlined">expand_more</span>	
				</Link>
			</div>
		</nav>
		</>
	);
};
