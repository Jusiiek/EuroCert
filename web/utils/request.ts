import type { RequestParams, RequestResponse } from "~/interfaces/request";
import { useAuth } from "~/composables/useAuth";

export const redirectIfNotAuthenticated = (res: Response) => {
  const { logout, forbidden } = useAuth();
  if (res.status === 401) logout();
  if (res.status === 403) forbidden();
};

export const encodeQuery = (query: Record<string, any>) => {
  const searchParams = new URLSearchParams(query || {});
  return searchParams.toString();
};

export const request = async ({
  url,
  query,
  headers = {},
  method = "GET",
  body,
  formData,
  skipRedirect = false,
  ...rest
}: RequestParams): Promise<RequestResponse> => {
  const methodLower = method.toLowerCase();
  const jsonMethods = ["post", "put", "patch", "delete"];
  if (body && jsonMethods.includes(methodLower) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const { getAuthToken } = useAuth();

  let requestBody: BodyInit | null | undefined = undefined;
  if (formData) {
    requestBody = formData;
  } else if (body) {
    if (typeof body === "object") {
      requestBody = JSON.stringify(body);
    } else {
      requestBody = body as BodyInit;
    }
  }
  const token = getAuthToken();
  if (token) {
    headers.Authorization = token;
  }

  if (query) {
    url = `${url}?${encodeQuery(query)}`;
  }
  const res = await fetch(url, {
    method: method,
    headers: headers,
    body: requestBody,
    credentials: "include",
    ...rest,
  });

  if (!skipRedirect) {
    redirectIfNotAuthenticated(res);
  }

  const contentType = res.headers.get("content-type");
  if (contentType !== "application/json" || res.status === 204) {
    return {
      res,
      data: {},
      headers: res.headers,
    };
  }

  const data = await res.json();

  return {
    res,
    data,
    headers: res.headers,
  };
};