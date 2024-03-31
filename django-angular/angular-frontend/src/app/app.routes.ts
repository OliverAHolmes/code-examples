import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { UsersListComponent } from './users-list/users-list.component';
import { UsersProfileComponent } from './users-profile/users-profile.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'users-list', component: UsersListComponent },
  { path: 'users-profile/:id', component: UsersProfileComponent },
  { path: '**', redirectTo: '' },
];
