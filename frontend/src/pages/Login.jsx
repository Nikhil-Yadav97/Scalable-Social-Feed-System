import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import {
    Avatar,
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Container,
    Stack,
    TextField,
    Typography
} from "@mui/material";

import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

import useAuth from "../hooks/useAuth";

export default function Login() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [form, setForm] = useState({
        email: "",
        password: ""
    });

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    function handleChange(e) {

        setForm({
            ...form,
            [e.target.name]: e.target.value
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        setLoading(true);

        setError("");

        try {

            await login(form);

            navigate("/");

        }

        catch (err) {

            setError(
                err.response?.data?.detail ||
                "Login failed"
            );

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <Container maxWidth="sm">

            <Box
                sx={{
                    minHeight: "100vh",
                    display: "flex",
                    alignItems: "center"
                }}
            >

                <Card sx={{ width: "100%" }}>

                    <CardContent>

                        <Stack
                            spacing={3}
                            alignItems="center"
                        >

                            <Avatar sx={{ bgcolor: "primary.main" }}>

                                <LockOutlinedIcon />

                            </Avatar>

                            <Typography
                                variant="h4"
                                fontWeight="bold"
                            >
                                Sign In
                            </Typography>

                            {error &&

                                <Alert
                                    severity="error"
                                    sx={{ width: "100%" }}
                                >

                                    {error}

                                </Alert>

                            }

                            <Box
                                component="form"
                                width="100%"
                                onSubmit={handleSubmit}
                            >

                                <Stack spacing={2}>

                                    <TextField
                                        label="Email"
                                        name="email"
                                        type="email"
                                        fullWidth
                                        required
                                        value={form.email}
                                        onChange={handleChange}
                                    />

                                    <TextField
                                        label="Password"
                                        name="password"
                                        type="password"
                                        fullWidth
                                        required
                                        value={form.password}
                                        onChange={handleChange}
                                    />

                                    <Button
                                        variant="contained"
                                        type="submit"
                                        disabled={loading}
                                        size="large"
                                    >

                                        {loading ?

                                            <CircularProgress
                                                size={24}
                                                color="inherit"
                                            />

                                            :

                                            "Login"

                                        }

                                    </Button>

                                </Stack>

                            </Box>

                            <Typography>

                                Don't have an account?{" "}

                                <Link to="/register">

                                    Register

                                </Link>

                            </Typography>

                        </Stack>

                    </CardContent>

                </Card>

            </Box>

        </Container>

    );

}