import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, RouterLink } from '@angular/router'; // Import ActivatedRoute

@Component({
  selector: 'app-users-profile',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './users-profile.component.html',
  styleUrls: ['./users-profile.component.css'], // Corrected property name to styleUrls
})
export class UsersProfileComponent implements OnInit {
  user: any;
  id: any;

  constructor(
    private userService: UserService,
    private route: ActivatedRoute // Inject ActivatedRoute
  ) {}

  ngOnInit(): void {
    // Use ActivatedRoute to get the id parameter
    this.id = this.route.snapshot.paramMap.get('id');

    if (this.id) {
      this.userService.getUser(this.id).then((user) => {
        // Ensure this.id is passed
        this.user = user;
        console.log(this.user);
      });
    } else {
      console.error('No ID found in URL');
    }
  }
}
