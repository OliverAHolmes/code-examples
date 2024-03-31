import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  url = 'http://127.0.0.1:8000/users/';

  async getUsers(): Promise<any[]> {
    const data = await fetch(this.url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });
    return (await data.json()) ?? [];
  }

  async getUser(id: number): Promise<any> {
    const data = await fetch(`${this.url}${id}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });
    return await data.json();
  }
}
