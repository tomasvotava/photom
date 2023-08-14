import { PUBLIC_API_URL } from '$env/static/public';

// @ts-ignore
import * as Types from '$lib/types.js';

export class ApiClient {
	/**
	 *
	 * @param {String=} baseUrl
	 */
	constructor(baseUrl) {
		this.baseUrl = baseUrl || 'http://localhost:3000';
	}

	/**
	 *
	 * @param {String} path Path
	 * @returns {Promise<any>} Response
	 */
	async get(path) {
		const response = await fetch(`${this.baseUrl}${path}`);
		return await response.json();
	}

	/**
	 *
	 * @param {String} path Path
	 * @param {Object} body Payload
	 * @returns {Promise<Object>} Response
	 */
	async post(path, body) {
		const response = await fetch(`${this.baseUrl}${path}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});
		return await response.json();
	}

	/**
	 * List accounts from the store
	 * @returns {Promise<Types.Account[]>} Array of accounts
	 */
	async listAccounts() {
		return await this.get('/auth/');
	}

	/**
	 * Delete account by email
	 * @param {String} email
	 * @returns empty response
	 */
	async deleteAccount(email) {
		return await fetch(`${this.baseUrl}/auth/${email}`, { method: 'DELETE' });
	}
}

export const defaultClient = new ApiClient(PUBLIC_API_URL);
