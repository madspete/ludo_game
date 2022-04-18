import ludopy
import numpy as np
import cv2
from ludopy.player import get_enemy_at_pos, enemy_pos_at_pos
from stateAndActions import StateAndActions

g = ludopy.Game()
there_is_a_winner = False

round = 0
while not there_is_a_winner:

    input_states = StateAndActions()
    (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
    pieces = enemy_pieces
    pieces = np.append(enemy_pieces, [player_pieces], axis=0)
    if player_i == 1:
        if len(move_pieces):
            home = input_states.home(player_pieces)
            goal_zone = input_states.goal_zone(player_pieces)
            unsafe = input_states.unsafe(player_pieces, enemy_pieces)
            danger = input_states.in_danger(player_pieces, enemy_pieces)
            goal = input_states.goal(player_pieces)
            safe = input_states.safe(player_pieces)
            can_die = input_states.can_die(player_pieces, dice, enemy_pieces)
            print(dice)
            print(f"can die {input_states.can_die(player_pieces, dice, enemy_pieces)}")
            print(f"can get on globe {input_states.can_get_on_globe(pieces, dice, can_die)}")
            print(f"can get on star {input_states.can_reach_star(pieces, dice, can_die)}")
            print(f"can reach goal {input_states.can_reach_goal_zone(pieces, dice)}")
            print(f"can get out of home {input_states.can_get_out_of_home(pieces, dice)}")
            print(f"can kill an enemy {input_states.can_kill(pieces, dice, enemy_pieces, can_die)}")
            print(f"can protect {input_states.can_protect(pieces, dice)}")
            print(f"can reach goal {input_states.can_reach_goal(pieces, dice)}")
            print(f"can move out off danger {input_states.move_out_of_danger(pieces, dice, danger)}")
            print(f"can move piece clostes to home {input_states.move_closets_piece(pieces, dice, can_die)}")
            print(f"can move piece clostes to home {input_states.miss_goal(pieces, dice, goal_zone)}")

            if len(move_pieces) == 4:
                enemy_at_pos, enemy_list = get_enemy_at_pos(27, enemy_pieces)
                print(f"enemies at pos {enemy_at_pos} and list {enemy_list}")
                print(f"positions of the pieces {player_pieces}")
                print(f"Availabe pieces to move {move_pieces}, chose one of them")
                img = ludopy.visualizer.make_img_of_board(pieces, dice, 3, round)
                img = cv2.resize(img, (1088,900))
                cv2.imshow("current board", img)
                waitkey = cv2.waitKey(0) 
                cv2.destroyAllWindows()
                piece_to_move = None
                if int(waitkey) == 48:
                    piece_to_move = move_pieces[0]
                elif int(waitkey) == 49:
                    piece_to_move = move_pieces[1]
                elif int(waitkey) == 50:
                    piece_to_move = move_pieces[2]
                elif int(waitkey) == 51:
                    piece_to_move = move_pieces[3]

                if piece_to_move == None:
                    raise Exception("invalid input")
            else:
                enemy_at_pos, enemy_list = get_enemy_at_pos(27, enemy_pieces)
                print(f"enemies at pos {enemy_at_pos} and list {enemy_list}")
                print(f"positions of the pieces {player_pieces}")
                print(f"Availabe pieces to move {move_pieces}, chose one of them")
                waitkeys = []
                for i in range(len(move_pieces)):
                    waitkeys.append((i, move_pieces[i] + 48))

                img = ludopy.visualizer.make_img_of_board(pieces, dice, 3, round)
                img = cv2.resize(img, (1088,900))
                cv2.imshow("current board", img)
                waitkey = cv2.waitKey(0) 
                cv2.destroyAllWindows()
                piece_to_move = None
                for i in range(len(waitkeys)):
                    (idx,key) = waitkeys[i]
                    if key == waitkey:
                        piece_to_move = move_pieces[idx]
                        break
                
                if piece_to_move == None:
                    raise Exception("Invalid input")

        else:
            piece_to_move = -1

        dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner = g.answer_observation(piece_to_move)      
    else:
        if len(move_pieces):
            piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1

        _, _, _, _, _, there_is_a_winner = g.answer_observation(piece_to_move)
    
    round = round + 1


print("Saving history to numpy file")
g.save_hist(f"game_history.npy")
print("Saving game video")
g.save_hist_video(f"game_video.avi")