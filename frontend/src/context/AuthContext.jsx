import { createContext, useEffect, useState } from "react";
import { login as loginApi, me } from "../api/auth";

export const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadUser();

    }, []);

    async function loadUser() {

        const token = localStorage.getItem("token");

        if (!token) {

            setLoading(false);

            return;
        }

        try {

            const data = await me();

            setUser(data);

        }

        catch {

            localStorage.removeItem("token");

            setUser(null);

        }

        finally {

            setLoading(false);

        }
    }

    async function login(credentials) {

        const data = await loginApi(credentials);

        localStorage.setItem(
            "token",
            data.access_token
        );

        const currentUser = await me();

        setUser(currentUser);

        return currentUser;

    }

    function logout() {

        localStorage.removeItem("token");

        setUser(null);
    }

    return (

        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}