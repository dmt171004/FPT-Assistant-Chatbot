export interface AuthUser {
  id: string;
  fullName: string;
  email: string;
}

export interface LoginResponse {
  token: string;
  user: AuthUser;
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function mockLogin(
  email: string,
  password: string,
): Promise<LoginResponse> {
  await delay(1000);
  if (!email || !password) throw new Error("Email and password are required");
  return {
    token: "mock-jwt-token-" + Date.now(),
    user: { id: "u1", fullName: "Proctor User", email },
  };
}

export async function mockRegister(
  fullName: string,
  email: string,
  password: string,
): Promise<{ success: boolean }> {
  await delay(1000);
  if (!fullName || !email || !password)
    throw new Error("All fields are required");
  return { success: true };
}

export async function mockSendOtp(
  email: string,
): Promise<{ success: boolean }> {
  await delay(1000);
  return { success: true };
}

export async function mockVerifyOtp(
  email: string,
  otp: string,
): Promise<{ success: boolean }> {
  await delay(1000);
  if (otp.length !== 6) throw new Error("Invalid OTP");
  return { success: true };
}

export async function mockResetPassword(
  password: string,
): Promise<{ success: boolean }> {
  await delay(1000);
  return { success: true };
}
