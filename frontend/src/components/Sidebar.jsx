import {
    Drawer,
    Toolbar,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText
} from "@mui/material";

import HomeIcon from "@mui/icons-material/Home";
import PersonIcon from "@mui/icons-material/Person";

import { Link } from "react-router-dom";

export default function Sidebar({
    mobile,
    open,
    setOpen,
    drawerWidth
}) {

    const content = (

        <>
            <Toolbar />

            <List>

                <ListItemButton
                    component={Link}
                    to="/"
                >

                    <ListItemIcon>

                        <HomeIcon />

                    </ListItemIcon>

                    <ListItemText primary="Feed" />

                </ListItemButton>

                <ListItemButton
                    component={Link}
                    to="/profile/me"
                >

                    <ListItemIcon>

                        <PersonIcon />

                    </ListItemIcon>

                    <ListItemText primary="Profile" />

                </ListItemButton>

            </List>
        </>

    );

    if (mobile) {

        return (

            <Drawer
                open={open}
                onClose={() => setOpen(false)}
            >

                {content}

            </Drawer>

        );

    }

    return (

        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                "& .MuiDrawer-paper": {
                    width: drawerWidth
                }
            }}
        >

            {content}

        </Drawer>

    );

}