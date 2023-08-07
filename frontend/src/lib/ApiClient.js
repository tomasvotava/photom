import { PUBLIC_API_URL } from '$env/static/public';

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
	 * @returns {Promise<Object>} Response
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
}

export const defaultClient = new ApiClient(PUBLIC_API_URL);
