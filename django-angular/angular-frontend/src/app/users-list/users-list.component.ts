import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-users-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './users-list.component.html',
  styleUrls: ['./users-list.component.css'],
})
export class UsersListComponent implements OnInit {
  users: any[] = [];

  constructor(private router: Router, private userService: UserService) {}

  navigateHome() {
    this.router.navigate(['/']);
  }

  ngOnInit(): void {
    this.userService.getUsers().then((users) => {
      this.users = users;
      console.log(this.users);
    });
  }
}
