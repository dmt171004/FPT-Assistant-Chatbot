import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { toast } from "sonner";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type VerifyResponse = {
  message: string;
  username: string;
  email: string;
};

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<VerifyResponse | null>(null);
  const [error, setError] = useState("");

  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setError("Invalid verification link");
      setLoading(false);
      return;
    }

    api
      .get(`/api/v1/auth/verify-email?token=${token}`)
      .then((res) => {
        setData(res.data);
        toast.success("Email verified successfully!");
      })
      .catch((err) => {
        const msg =
          err.response?.data?.detail ||
          "Verification failed or token expired";

        setError(msg);
        toast.error(msg);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <Card className="w-full max-w-md shadow-chat">
        <CardContent className="space-y-6 p-8 text-center">

          {loading && (
            <>
              <h2 className="text-2xl font-bold">Verifying email...</h2>
              <p className="text-muted-foreground">
                Please wait while we verify your account.
              </p>
            </>
          )}

          {!loading && error && (
            <>
              <h2 className="text-2xl font-bold text-red-500">
                Verification Failed
              </h2>

              <p className="text-muted-foreground">{error}</p>

              <Button
                className="w-full"
                onClick={() => navigate("/login")}
              >
                Go to Login
              </Button>
            </>
          )}

          {!loading && data && (
            <>
              <h2 className="text-2xl font-bold text-green-600">
                Email Verified 
              </h2>

              <div className="text-sm text-muted-foreground space-y-1">
                <p>
                  <strong>Username:</strong> {data.username}
                </p>

                <p>
                  <strong>Email:</strong> {data.email}
                </p>
              </div>

              <Button
                className="w-full"
                onClick={() => navigate("/login")}
              >
                Go to Login
              </Button>
            </>
          )}

        </CardContent>
      </Card>
    </div>
  );
}