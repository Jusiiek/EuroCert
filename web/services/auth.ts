import { getApiUrl } from "~/services/config";
import { request } from "~/utils/request";
import type { RequestResponse } from "~/interfaces/request";
import type { AuthInterface } from "~/interfaces/auth";
import type { ServiceReturnInterface } from "~/interfaces/services";
import { ActiveUser } from "~/services/active_user";

class Auth {
    async register(body: object): Promise<RequestResponse> {
        return await request({
            url: `${getApiUrl()}/auth/register`,
            method: "POST",
            body
        })
    }

    async login(body: AuthInterface): Promise<ServiceReturnInterface> {
        const { res, data} = await request({
            url: `${getApiUrl()}/auth/login`,
            method: "POST",
            skipRedirect: true,
            body,
        });
        if (res.status === 200) {
            ActiveUser.setToken(data);
        }
        return {
            res,
            data
        };
    }
}

export const AuthServices = new Auth();