import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      await api.post("/api/v1/auth/register", {
        username,
        password,
      });

      alert("Register successful! Please login.");
      navigate("/login");
    } catch (error: any) {
      console.error(error);
      alert(error.response?.data?.detail || "Register failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <Card className="w-full max-w-md shadow-chat">
        <CardContent className="space-y-6 p-8">
          <h2 className="text-2xl font-bold text-center">Register</h2>

          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button className="w-full" onClick={handleRegister}>
            Create Account
          </Button>

          <p className="text-sm text-center text-muted-foreground">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-primary font-medium hover:underline"
            >
              Login here
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}