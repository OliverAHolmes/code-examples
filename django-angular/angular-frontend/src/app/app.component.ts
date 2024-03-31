import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { UsersListComponent } from './users-list/users-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, UsersListComponent, RouterModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'angular-frontend';
}
