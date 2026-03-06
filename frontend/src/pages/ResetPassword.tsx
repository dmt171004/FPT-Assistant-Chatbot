import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<any>({});

  const handleReset = async () => {

    setErrors({});

    if (password !== confirmPassword) {
      setErrors({ confirm_password: "Passwords do not match" });
      toast.error("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      await api.post("/api/v1/auth/reset-password", {
        token,
        new_password: password,
        confirm_password: confirmPassword,
      });

      toast.success("Password reset successful!");
      navigate("/login", { replace: true });

    } catch (error: any) {

      const details = error.response?.data?.detail;

      if (Array.isArray(details)) {

        const fieldErrors: any = {};

        details.forEach((err: any) => {
          const field = err.loc?.[1];
          fieldErrors[field] = err.msg;
        });

        setErrors(fieldErrors);

      } else {

        toast.error(details || "Invalid or expired token");

      }

    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        Invalid reset link.
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <Card className="w-full max-w-md shadow-chat">
        <CardContent className="space-y-6 p-8">

          <h2 className="text-2xl font-bold text-center">
            Reset Password
          </h2>

          {/* NEW PASSWORD */}

          <div className="space-y-1">
            <Input
              type="password"
              placeholder="New Password (at least 6 characters)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={errors.new_password ? "border-red-500" : ""}
            />

            {errors.new_password && (
              <p className="text-red-500 text-sm">
                {errors.new_password}
              </p>
            )}
          </div>

          {/* CONFIRM PASSWORD */}

          <div className="space-y-1">
            <Input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className={errors.confirm_password ? "border-red-500" : ""}
            />

            {errors.confirm_password && (
              <p className="text-red-500 text-sm">
                {errors.confirm_password}
              </p>
            )}
          </div>

          <Button
            className="w-full"
            onClick={handleReset}
            disabled={loading}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </Button>

        </CardContent>
      </Card>
    </div>
  );
}