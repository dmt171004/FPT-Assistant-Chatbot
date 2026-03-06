import { useState } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);

      const res = await api.post("/api/v1/auth/forgot-password", {
        email,
      });

      toast.success(res.data.message);
    } catch (error: any) {
      toast.error(
        error.response?.data?.detail?.[0]?.msg ||
        error.response?.data?.detail ||
        "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <Card className="w-full max-w-md shadow-chat">
        <CardContent className="space-y-6 p-8">
          <h2 className="text-2xl font-bold text-center">
            Forgot Password
          </h2>

          <Input
            placeholder="Enter your email (@fpt.edu.vn or @fe.edu.vn)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <Button
            className="w-full"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </Button>

          <p className="text-sm text-center text-muted-foreground">
            Back to{" "}
            <Link
              to="/login"
              className="text-primary font-medium hover:underline"
            >
              Login
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}