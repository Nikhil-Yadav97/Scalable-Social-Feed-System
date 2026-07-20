import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Button,
    Box
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";

import { Link } from "react-router-dom";

import useAuth from "../hooks/useAuth";

export default function Navbar({
    mobile,
    setOpen
}) {

    const { logout } = useAuth();

    return (

        <AppBar position="fixed">

            <Toolbar>

                {mobile && (

                    <IconButton
                        color="inherit"
                        onClick={() => setOpen(true)}
                    >

                        <MenuIcon />

                    </IconButton>

                )}

                <Typography
                    variant="h6"
                    sx={{ flexGrow: 1 }}
                >
                    Social Feed
                </Typography>

                {!mobile && (

                    <Box>

                        <Button
                            color="inherit"
                            component={Link}
                            to="/"
                        >
                            Feed
                        </Button>

                        <Button
                            color="inherit"
                            onClick={logout}
                        >
                            Logout
                        </Button>

                    </Box>

                )}

            </Toolbar>

        </AppBar>

    );

}