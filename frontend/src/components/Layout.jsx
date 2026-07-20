import { useState } from "react";

import {
    Box,
    Toolbar,
    useMediaQuery
} from "@mui/material";

import { useTheme } from "@mui/material/styles";

import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

const drawerWidth = 240;

export default function Layout({ children }) {

    const theme = useTheme();

    const mobile = useMediaQuery(theme.breakpoints.down("md"));

    const [open, setOpen] = useState(false);

    return (

        <Box sx={{ display: "flex" }}>

            <Navbar
                mobile={mobile}
                open={open}
                setOpen={setOpen}
            />

            <Sidebar
                mobile={mobile}
                open={open}
                setOpen={setOpen}
                drawerWidth={drawerWidth}
            />

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3
                }}
            >

                <Toolbar />

                {children}

            </Box>

        </Box>

    );
}