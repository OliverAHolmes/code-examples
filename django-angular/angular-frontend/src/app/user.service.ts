import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  url = 'http://127.0.0.1:8000/users/?format=json';

  async getUsers(): Promise<any[]> {
    const data = await fetch(this.url);
    console.log(data);
    return (await data.json()) ?? [];
  }

  // async getHousingLocationById(
  //   id: number
  // ): Promise<HousingLocation | undefined> {
  //   const data = await fetch(`${this.url}/${id}`);
  //   return (await data.json()) ?? {};
  // }

  // submitApplication(firstName: string, lastName: string, email: string) {
  //   console.log(firstName, lastName, email);
  // }
}
