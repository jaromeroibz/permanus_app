import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";
import { Brazaletes } from "./pages/Brazaletes";
import { Colecciones } from "./pages/Colecciones";
import { Collares } from "./pages/Collares";
import { Anillos } from "./pages/Anillos";
import { EdicionLimitada } from "./pages/EdicionLimitada";
import { Piercings } from "./pages/Piercings";
import { Tobilleras } from "./pages/Tobilleras";
import { Home } from "./pages/home";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import injectContext from "./store/appContext";
import { Header } from "./component/header";
import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import { Signup } from "./component/signup";


//create your first component
const Layout = () => {
    //the basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";

    if(!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL/ >;

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Header/>
                    <Navbar />
                    <Routes>
                        <Route element={<Home />} path="/" />
                        <Route element={<Signup />} path="/signup" />
                        <Route element={<Brazaletes />} path="/brazaletes" />
                        <Route element={<Collares />} path="/collares" />
                        <Route element={<Anillos />} path="/anillos" />
                        <Route element={<Colecciones />} path="/colecciones" />
                        <Route element={<EdicionLimitada />} path="/edicionlimitada" />
                        <Route element={<Piercings />} path="/piercings" />
                        <Route element={<Tobilleras />} path="/tobilleras" />
                        <Route element={<Demo />} path="/demo" />
                        <Route element={<Single />} path="/single/:theid" />
                        <Route element={<h1>Not found!</h1>} />
                    </Routes>
                    <Footer />
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
