export interface TokenInterface {
    access_token: string;
    token_type: string
}

export const tokenKey = "euro_cert_token";


class User {
    private tokenData: TokenInterface | null = null;

    get() {
        if (process.client) {
            const savedToken = localStorage.getItem(tokenKey);
            if (savedToken) {
                this.tokenData = JSON.parse(savedToken);
                if (this.tokenData)
                    this.setToken(this.tokenData);
                return this.tokenData;
            }
        }
    }

    setToken(tokenData: TokenInterface) {
        if (process.client) {
            localStorage.setItem(tokenKey, JSON.stringify(tokenData));
            this.tokenData = tokenData
        }
    }

    clear() {
        if (process.client) {
            localStorage.removeItem(tokenKey);
            this.tokenData = null;
        }
    }

    getToken() {
        this.get()
        return this.tokenData?.access_token;
    }

    getTokenType() {
        this.get()
        return this.tokenData?.token_type;
    }
}

export const ActiveUser = new User();